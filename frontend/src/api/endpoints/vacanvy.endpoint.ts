import api from "api/utils/api";
import { Query } from "../utils/buildQueryString";
import { VacancyDto } from "../models/vacancy.model";
import { paged } from "../models/paged.model";

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
}
