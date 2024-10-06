import { z } from "zod";

export namespace TaskDto {
  export const Item = z.object({
    vacancy_name: z.string(),
    stage_name: z.string(),
    stage_url: z.string(),
    candidate_id: z.number(),
    deadline: z.string(),
  });
  export type Item = z.infer<typeof Item>;
}
