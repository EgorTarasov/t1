import { VacancyEndpoint } from "@/api/endpoints/vacanvy.endpoint";
import { VacancyDto } from "@/api/models/vacancy.model";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable } from "mobx";

export class VacanciesStore implements DisposableVm {
  constructor() {
    makeAutoObservable(this);
  }

  items: VacancyDto.Item[] = [];
  async init() {
    const res = await VacancyEndpoint.list({
      page: 1,
      size: 100,
    });
    this.items = res.items;
  }

  dispose() {
    console.log("dispose");
  }
}
