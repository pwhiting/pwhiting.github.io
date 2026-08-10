# Using Google Photos in blog posts

Use normal Google Photos share links everywhere. Do **not** convert them to
`lh3.googleusercontent.com` links yourself.

## Before you start

In Google Photos, open the picture, choose **Share**, then **Create link** (if
needed) and **Copy link**. The link should begin like this:

```text
https://photos.app.goo.gl/...
```

Keep the photo shared with anyone who has the link. If the link is made private
or deleted, the site build stops rather than publishing a broken image.

## Add a hero image

Put the Google Photos share link in the post's front matter:

```yaml
---
layout: post
title: My post title
date: 2026/08/10
image: https://photos.app.goo.gl/your-share-link
---
```

The hero image is centered by default. To choose a different part of the image
as the focal point, add `image_position` with horizontal and vertical values:

```yaml
image_position: "65% 35%"
```

`50% 50%` is the default (centered). The first number moves the focal point
left/right; the second moves it up/down.

## Copy-and-paste examples for post text

Use ordinary Markdown and paste the appropriate Google Photos share link. The
description between `[]` is useful for accessibility and becomes the image
caption on the post.

### One photo (a static image)

```md
![A short description of the photo](https://photos.app.goo.gl/your-photo-link)
```

This displays the photo in the post. It is not clickable.

### An album cover that opens the album

```md
![Open the photo album](https://photos.app.goo.gl/your-album-link){:target="_blank"}
```

The site displays the album cover and makes it clickable. The added
`{:target="_blank"}` is the signal that this is an album or video link. A quiet
note beneath it says that Google Photos opens in a new tab. Do not wrap this in
another link.

### A video preview that opens the video

```md
![Watch the video](https://photos.app.goo.gl/your-video-link){:target="_blank"}
```

The site displays the video's preview image and makes it clickable. Selecting
it opens the video in a new tab; the quiet note beneath it makes that clear.

## What happens when you publish

When the site builds, it finds these Google Photos links and converts them to
the embeddable image URLs needed by the web page. Regular Google Photos images
stay within the post. Images marked with `{:target="_blank"}` open their Google
Photos share page in a new tab, with a quiet note underneath the preview making
that clear. Your Markdown and front matter stay in the easy-to-edit
`photos.app.goo.gl` form, so there is no extra conversion step for you.

## Full example

```md
---
layout: post
title: Family visit
date: 2026/08/09
category: Family
image: https://photos.app.goo.gl/your-hero-photo
image_position: "50% 50%"
---

Nice family visit yesterday - it was great to see MJ and fam.

![Everyone together](https://photos.app.goo.gl/your-in-post-photo)
```
