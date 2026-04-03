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
  filePath: string | undefined,
  includeBase = true
) {
  if (!filePath) return `/${id}`;

  const normalizedPath = filePath.replaceAll("\\", "/");
  const normalizedBlogPath = BLOG_PATH.replaceAll("\\", "/");
  const relativePath = normalizedPath.replace(normalizedBlogPath, "").replace(/^\/+/, "");
  const segments = relativePath.split("/");
  const filename = segments.pop() || "";
  const slug = filename.replace(/\.md$/, "");

  if (!includeBase) {
    return slug;
  }

  return "/" + [...segments, slug].join("/");
}
