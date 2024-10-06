import { VacancyStore } from "@/stores/vanacy.store";
import { observer } from "mobx-react-lite";
import { FC } from "react";

interface Props {
  vm: VacancyStore;
}

const Card: FC<{
  title: string;
  value: string;
}> = observer((x) => {
  return (
    <div className="font-medium rounded-xl p-4 bg-white flex flex-col gap-2">
      <h3 className="text-xl">{x.value}</h3>
      <p className="text-nowrap">{x.title}</p>
    </div>
  );
});

export const AnalyticsView: FC<Props> = observer((x) => {
  return (
    <div className="flex flex-wrap gap-4">
      <Card title="Наполненность рынка" value="чел. на вакансию" />
      <Card title="Диапазон ожиданий по ЗП" value="МЛН – МЛН" />
      <Card title="Медиальное значение по ожидаемой ЗП" value="МЛН" />
      <Card title="Диапазон по ЗП у конкурентов" value="МЛН – МЛН" />
      <Card title="Медиальное значение по ЗП у конкурентов" value="МЛН – МЛН" />
    </div>
  );
});
