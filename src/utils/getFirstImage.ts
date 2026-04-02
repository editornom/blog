/**
 * Extracts the first image URL from a markdown string.
 * Returns the path as found in the markdown.
 * If no image is found, returns a fallback test image path.
 * @param body The markdown content of the post.
 * @returns The path of the first image or a fallback test image.
 */
export function getFirstImage(body: string): string {
  // Regex for Markdown images: ![alt](url)
  const mdImageRegex = /!\[.*?\]\((.*?)\)/;
  // Regex for HTML images: <img src="url" ...>
  const htmlImageRegex = /<img.*?src=["'](.*?)["'].*?>/;

  const mdMatch = body.match(mdImageRegex);
  if (mdMatch && mdMatch[1]) {
    return mdMatch[1].split(" ")[0]; // Return the path directly
  }

  const htmlMatch = body.match(htmlImageRegex);
  if (htmlMatch && htmlMatch[1]) {
    return htmlMatch[1];
  }

  // Fallback: Default test image basename
  const randomNum = Math.floor(Math.random() * 4) + 1;
  return `@/assets/images/test-${randomNum}.png`;
}

export default getFirstImage;
