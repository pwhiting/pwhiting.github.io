# Google Photos in posts

Use the normal Google Photos share link as the only image URL you type.

For a post header image, put the share link in `image`:

```yaml
image: https://photos.app.goo.gl/your-share-link
```

Hero images use `50% 50%` (horizontal then vertical) by default. If a
particular photo needs a different focal point, add both percentages to its
front matter, for example: `image_position: "65% 35%"`.

For an image in the post, use ordinary Markdown:

```md
![A short description](https://photos.app.goo.gl/your-share-link)
```

When the site publishes, the build replaces that URL with the current public
image URL and makes the image open its Google Photos share page when selected.
The source post remains unchanged.  Leave the photo shared publicly in Google
Photos; a private or deleted share link will stop the build so it is not
published with a broken image.
