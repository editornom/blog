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
  // Also strip YYMMDD_ prefix from any path segment to keep URLs clean
  const normalizedId = id
    .replace(/\\/g, "/")
    .replace(/\.(md|mdx)$/, "")
    .replace(/(^|\/)\d{6}_/g, "$1");
    
  const segments = normalizedId.split("/");
  const slug = segments.pop() || "";

  if (!includeBase) {
    // If we only need the slug/sub-path without base prefix, for haionnet we strip 'haionnet/' as well if needed
    if (normalizedId.startsWith("haionnet/")) {
      return normalizedId.replace("haionnet/", "");
    }
    return slug;
  }

  // Prepend /ko/ for haionnet posts so they are mapped to the Korean haionnet board
  if (normalizedId.startsWith("haionnet/")) {
    return "/ko/" + normalizedId;
  }

  // Prepend / for absolute internal URL
  return "/" + normalizedId;
}
