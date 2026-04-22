import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";
import { SITE } from "@/config";

export const BLOG_PATH = "src/data/blog";

const blog = defineCollection({
  loader: glob({ 
    pattern: "**/[^_]*.md", 
    base: `./${BLOG_PATH}`,
    generateId: ({ entry }) => entry.replace(/\\/g, "/")
  }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(SITE.author),
      pubDatetime: z.date(),
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      slug: z.string(),
      featured: z.boolean().optional(),
      draft: z.boolean().optional(),
      tags: z.array(z.string()).default(["others"]).optional(),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
      faqs: z.array(z.object({
        q: z.string(),
        a: z.string(),
      })).optional(),
      references: z.array(z.string()).optional(),
    }),
});

export const collections = { blog };
