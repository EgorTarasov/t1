import { z } from "zod";
import { paged } from "./paged.model";
import { Priority } from "@/types/priority.type";
//  "id": 0,
//   "name": "string",
//   "priority": 0,
//   "deadline": "2024-10-05T15:19:44.255Z",
//   "profession": "string",
//   "area": "string",
//   "supervisor": "string",
//   "city": "string",
//   "experience_from": 0,
//   "experience_to": 0,
//   "education": "string",
//   "quantity": 0,
//   "description": "string",
//   "type_of_employment": "string",
//   "vacancy_skills": [
//     {
//       "name": "Python",
//       "id": 1
//     }
//   ]

export namespace VacancyDto {
  export const Item = z.object({
    id: z.number(),
    name: z.string(),
    priority: Priority.Schema,
    deadline: z.string(),
    profession: z.string(),
    area: z.string(),
    supervisor: z.string(),
  });
  export type Item = z.infer<typeof Item>;
}
