import { z } from "zod";
import { VacancyDto } from "./vacancy.model";

export namespace CandidatesDto {
  export const Candidate = z.object({
    candidate_id: z.number(),
    source: z.string(),
    similarity: z.number(),
  });
  export type Candidate = z.infer<typeof Candidate>;

  export const ActiveCandidate = Candidate.extend({
    stage_name: z.string(),
    date_of_accept: z.string(),
  });
  export type ActiveCandidate = z.infer<typeof ActiveCandidate>;

  export const DeclinedCandidate = Candidate.extend({
    date_of_decline: z.string(),
    reason: z.string(),
  });
  export type DeclinedCandidate = z.infer<typeof DeclinedCandidate>;

  export const PotentialCandidate = z.object({
    source: z.string(),
    similarity: z.number(),
  });
  export type PotentialCandidate = z.infer<typeof PotentialCandidate>;
}
