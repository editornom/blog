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
      pubDatetime: z.coerce.date(),
      modDatetime: z.coerce.date().optional().nullable(),
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
      // 토픽 클러스터 소속 (scripts/topics.yaml 의 id).
      // 내부 링크 연결과 다음 주제 선정이 이 값을 읽습니다.
      cluster: z.string().optional(),
      // 이 글이 답하는 질문. 같은 클러스터 안에서 중복 주제를 피하는 데 씁니다.
      question: z.string().optional(),
      references: z.array(z.string()).optional(),
    }),
});

export const collections = { blog };
