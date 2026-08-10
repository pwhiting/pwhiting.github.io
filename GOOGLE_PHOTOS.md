# Google Photos in posts

Use the normal Google Photos share link as the only image URL you type.

For a post header image, put the share link in `image`:

```yaml
image: https://photos.app.goo.gl/your-share-link
```

For an image in the post, use ordinary Markdown:

```md
![A short description](https://photos.app.goo.gl/your-share-link)
```

When the site publishes, the build replaces that URL with the current public
image URL and makes the image open its Google Photos share page when selected.
The source post remains unchanged.  Leave the photo shared publicly in Google
Photos; a private or deleted share link will stop the build so it is not
published with a broken image.
