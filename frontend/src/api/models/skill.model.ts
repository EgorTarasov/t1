import { z } from "zod";

export namespace SkillDto {
  export const Item = z.object({
    name: z.string(),
    id: z.number(),
  });
  export type Item = z.infer<typeof Item>;
}
