import { z } from "zod";
import { CandidatesDto } from "../models/candidates.model";
import api from "../utils/api";

export namespace CandidatesEndpoint {
  export const getActiveCandidates = (vacancyId: number) =>
    api.get(`/vacancies/candidates/active/${vacancyId}`, {
      schema: z.object({
        candidates: z.array(CandidatesDto.ActiveCandidate),
      }),
    });

  export const getDeclinedCandidates = (vacancyId: number) =>
    api.get(`/vacancies/candidates/declined/${vacancyId}`, {
      schema: z.object({
        candidates: z.array(CandidatesDto.DeclinedCandidate),
      }),
    });

  export const getPotentialCandidates = (vacancyId: number) =>
    api.get(`/vacancies/candidates/potential/${vacancyId}`, {
      schema: z.object({
        candidates: z.array(CandidatesDto.PotentialCandidate),
      }),
    });

  export const getAnalytics = (vacancyId: number) =>
    api.get(`/vacancies/stats/${vacancyId}`, {
      schema: CandidatesDto.Analytics,
    });
}
