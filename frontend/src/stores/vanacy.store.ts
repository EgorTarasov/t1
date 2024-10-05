import { mockVacancy, VacancyDto } from "@/api/models/vacancy.model";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable, observable } from "mobx";

export class VacancyStore implements DisposableVm {
  tab = "overview";

  constructor(public readonly vacancy: VacancyDto.DetailedItem) {
    makeAutoObservable(this);
  }

  dispose(): void {}
}
