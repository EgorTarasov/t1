// {
//   "items": [
//   ],
//   "total": 0,
//   "page": 1,
//   "size": 1,
//   "pages": 0
// }

import { z } from "zod";

export const paged = <T extends z.ZodType<any>>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    total: z.number(),
    page: z.number(),
    size: z.number(),
    pages: z.number(),
  });
