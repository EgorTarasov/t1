import api from "api/utils/api";
import { Query } from "../utils/buildQueryString";
import { VacancyDto } from "../models/vacancy.model";
import { paged } from "../models/paged.model";
import { z } from "zod";
import { Priority } from "@/types/priority.type";

export namespace VacancyEndpoint {
  export interface ListTemplate extends Query {
    isAppointed?: boolean;
    byDateDeadline?: boolean;
    byDateCreation?: boolean;
    byPriority?: boolean;
    page: number;
    size: number;
  }
  export const list = (search: ListTemplate) =>
    api.get("/vacancies/all/active", {
      search,
      schema: paged(VacancyDto.Item),
    });

  export const getById = (id: string) =>
    api.get(`/vacancies/${id}`, {
      schema: VacancyDto.DetailedItem,
    });

  interface VacancyTemplate {
    name: string;
    priority: Priority.Priority;
    deadline: Date;
    profession: string;
    area: string;
    supervisor: string;
    city: string;
    experienceFrom: string;
    experienceTo: string;
    education: string;
    keySkills: number[];
    additionalSkills: number[];
    description: string;
    typeOfEmployment: string;
    quantity: number;
    direction: string;
  }
  export const create = (vacancy: VacancyTemplate) =>
    api.post("/vacancies/new", vacancy, {
      schema: z.number(),
    });
}
