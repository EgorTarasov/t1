import { VacancyEndpoint } from "@/api/endpoints/vacanvy.endpoint";
import { VacancyDto } from "@/api/models/vacancy.model";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable } from "mobx";
import { buildFilterKey, Filter } from "./filter.vm";
import { Priority } from "@/types/priority.type";

const filterKeys: {
  getValue: (v: VacancyDto.Item) => string | null;
  name: string;
}[] = [
  {
    getValue: (v) => Priority.locale[v.priority],
    name: "Приоритет",
  },
  {
    getValue: (v) => v.city,
    name: "Локация",
  },
  {
    getValue: (v) => v.profession,
    name: "Профессия",
  },
];

export class VacanciesStore implements DisposableVm {
  filters: Filter<VacancyDto.Item>[] = [];

  constructor(public readonly items: VacancyDto.Item[]) {
    makeAutoObservable(this);
    const filters = new Map<string, Set<string>>();

    items.forEach((item) => {
      buildFilterKey(item, filterKeys, filters);
    });

    this.filters = Array.from(filters.entries()).map(
      ([name, values]) =>
        new Filter(
          name,
          Array.from(values),
          filterKeys.find((k) => k.name === name)!.getValue,
          () => this.filterItems(),
        ),
    );
  }

  filteredItems: VacancyDto.Item[] = this.items;

  filterItems() {
    this.filteredItems = this.items.filter((item) => {
      return this.filters.every((f) => f.values.includes(f.getValue(item)!));
    });
  }

  dispose() {
    console.log("dispose");
  }
}
