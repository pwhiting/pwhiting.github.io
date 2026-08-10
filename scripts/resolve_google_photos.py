#!/usr/bin/env python3
"""Prepare Google Photos links for a static Jekyll build.

Posts keep the durable share URL as their source of truth.  This program copies
the site to a build directory and replaces only Google Photos image sources
with the current public CDN image URL:

    image: https://photos.app.goo.gl/...
    ![Caption](https://photos.app.goo.gl/...)

Inline images stay in the post by default. Add `{:target="_blank"}` after an
album or video image to make that preview open its Google Photos page in a new
tab, followed by a brief explanatory note.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


GOOGLE_PHOTOS_URL = r"https?://(?:photos\.app\.goo\.gl|photos\.google\.com)/[^\s)\]<>\"']+"
FRONT_MATTER_IMAGE = re.compile(
    rf"^(?P<prefix>\s*(?:image|image2)\s*:\s*)(?P<quote>[\"']?)(?P<url>{GOOGLE_PHOTOS_URL})(?P=quote)(?P<end>\s*)$",
    re.MULTILINE,
)
MARKDOWN_IMAGE = re.compile(
    rf"!\[(?P<alt>[^\]]*)\]\((?P<url>{GOOGLE_PHOTOS_URL})\)(?P<attributes>\{{:[^\n}}]*\}})?",
)
OG_IMAGE = re.compile(
    r'<meta\s+property=["\']og:image["\']\s+content=["\'](?P<url>[^"\']+)["\']',
    re.IGNORECASE,
)

EXCLUDED_DIRS = {".git", ".bundle", ".build-source", "_site", "vendor"}


def fetch_embed_url(share_url: str) -> str:
    """Return the public image URL advertised by a Google Photos share page."""
    request = Request(
        share_url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; RideWhitingsPhotoResolver/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                page = response.read().decode("utf-8", errors="replace")
            match = OG_IMAGE.search(page)
            if not match:
                raise RuntimeError("Google Photos did not provide an og:image value")
            # Match the existing GPhoto Url app: discard Google's preview-size
            # suffix (for example, =w600-h315-p-k) and request the full image.
            image_url = html.unescape(match.group("url"))
            if not image_url.startswith("https://lh3.googleusercontent.com/"):
                raise RuntimeError("Google Photos og:image is not a public image URL")
            return image_url.split("=", 1)[0] + "=s0-no"
        except (URLError, OSError, RuntimeError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2**attempt)
    raise RuntimeError(str(last_error))


def convert_text(text: str, source_name: str, resolved: dict[str, str], failures: list[str]) -> str:
    def lookup(share_url: str) -> str | None:
        if share_url in resolved:
            return resolved[share_url]
        try:
            resolved[share_url] = fetch_embed_url(share_url)
            print(f"Resolved {share_url}", file=sys.stderr)
            return resolved[share_url]
        except RuntimeError as error:
            failures.append(f"{source_name}: {share_url} ({error})")
            return None

    def replace_front_matter(match: re.Match[str]) -> str:
        embed_url = lookup(match.group("url"))
        if not embed_url:
            return match.group(0)
        return f"{match.group('prefix')}{match.group('quote')}{embed_url}{match.group('quote')}{match.group('end')}"

    def replace_inline_image(match: re.Match[str]) -> str:
        share_url = match.group("url")
        alt = match.group("alt")
        embed_url = lookup(share_url)
        if not embed_url:
            return match.group(0)
        attributes = match.group("attributes") or ""
        image = f"![{alt}]({embed_url})"
        if 'target="_blank"' not in attributes and "target='_blank'" not in attributes:
            return image + attributes
        media_type = "album" if "album" in alt.casefold() else "video" if "video" in alt.casefold() else "link"
        return (
            f"[{image}]({share_url}){{:target=\"_blank\"}}\n\n"
            f'<p class="google-photos-note">({media_type} opens in a new tab)</p>'
        )

    text = FRONT_MATTER_IMAGE.sub(replace_front_matter, text)
    return MARKDOWN_IMAGE.sub(replace_inline_image, text)


def copy_site(source: Path, destination: Path) -> None:
    if destination.exists():
        raise RuntimeError(f"Destination already exists: {destination}")

    def ignore(path: str, names: list[str]) -> set[str]:
        return {name for name in names if name in EXCLUDED_DIRS or name == "Gemfile.lock"}

    shutil.copytree(source, destination, ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Jekyll source directory")
    parser.add_argument("--destination", type=Path, required=True, help="temporary prepared source directory")
    arguments = parser.parse_args()

    source = arguments.source.resolve()
    destination = arguments.destination.resolve()
    if not source.is_dir():
        parser.error(f"Source directory does not exist: {source}")
    if destination == source or source in destination.parents:
        parser.error("Destination must be outside the source directory")

    copy_site(source, destination)
    resolved: dict[str, str] = {}
    failures: list[str] = []
    for post in sorted((destination / "_posts").rglob("*.md")):
        original = post.read_text(encoding="utf-8")
        converted = convert_text(original, str(post.relative_to(destination)), resolved, failures)
        if converted != original:
            post.write_text(converted, encoding="utf-8")

    if failures:
        print("\nUnable to resolve these Google Photos links:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Prepared {len(resolved)} Google Photos image(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
