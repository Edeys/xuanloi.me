import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDatetime: z.date(),
    modDatetime: z.date().optional().nullable(),
    author: z.string().default("Đào Xuân Lợi"),
    category: z.string().default("Phát triển bản thân"),
    tags: z.array(z.string()).default(["others"]),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    unlisted: z.boolean().default(false),
    ogImage: z.string().optional(),
    heroImage: z.string().optional(),
    canonicalURL: z.string().optional(),
    hideEditPost: z.boolean().optional(),
    timezone: z.string().optional(),
    source: z.string().optional(),
    AIDescription: z.boolean().optional(),
    faq: z
      .array(
        z.object({
          question: z.string(),
          answer: z.string(),
        }),
      )
      .optional(),
  }),
});

export const collections = { blog };
