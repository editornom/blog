import { BLOG_PATH } from "@/content.config";
import { slugifyStr } from "./slugify";

/**
 * Get full path of a blog post
 * @param id - id of the blog post (aka slug)
 * @param filePath - the blog post full file location
 * @param includeBase - whether to include `/posts` in return value
 * @returns blog post path
 */
export function getPath(
  id: string,
  filePath: string | undefined, // Note: filePath might be undefined in Astro 5
  includeBase = true
) {
  // Normalize id: strip .md extension and handle backslashes
  const normalizedId = id.replace(/\\/g, "/").replace(/\.(md|mdx)$/, "");
  const segments = normalizedId.split("/");
  const slug = segments.pop() || "";

  if (!includeBase) {
    return slug;
  }

  // Prepend / for absolute internal URL
  return "/" + normalizedId;
}
