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
    getValue: (v) => v.city.toLowerCase(),
    name: "Локация",
  },
  {
    getValue: (v) => v.profession.toLowerCase(),
    name: "Профессия",
  },
];

export class VacanciesStore implements DisposableVm {
  filters: Filter<VacancyDto.Item>[] = [];

  constructor(public items: VacancyDto.Item[] | undefined) {
    makeAutoObservable(this);

    this.init();
  }

  async init() {
    if (!this.items) {
      const res = await VacancyEndpoint.list({ page: 1, size: 100 });
      this.items = res.items;
    }

    const filters = new Map<string, Set<string>>();

    this.items?.forEach((item) => {
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

    this.filterItems();
  }

  filteredItems: VacancyDto.Item[] = [];

  filterItems() {
    this.filteredItems =
      this.items?.filter((item) => {
        return this.filters.every((f) => f.values.includes(f.getValue(item)!));
      }) ?? [];
  }

  dispose() {
    console.log("dispose");
  }
}
