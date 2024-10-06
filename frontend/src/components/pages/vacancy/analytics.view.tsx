import { LoadingWrapper } from "@/components/ui/loaders/LoadingWrapper";
import { VacancyStore } from "@/stores/vanacy.store";
import { RussianRubleIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC, useEffect } from "react";

interface Props {
  vm: VacancyStore;
}

const Card: FC<{
  title: string;
  value: string;
  withRubles?: boolean;
}> = observer((x) => {
  return (
    <div className="font-medium rounded-xl p-4 bg-white flex flex-col gap-2">
      <h3 className="text-xl">{x.value}</h3>
      <div className="flex items-center gap-2">
        <p className="text-nowrap">{x.title}</p>
        {x.withRubles && <RussianRubleIcon className="size-4" />}
      </div>
    </div>
  );
});

export const AnalyticsView: FC<Props> = observer((x) => {
  useEffect(() => {
    x.vm.fetchAnalytics();
  }, [x.vm]);

  if (!x.vm.analytics) return <LoadingWrapper />;

  return (
    <div className="flex flex-wrap gap-4">
      <Card
        title="Наполненность рынка"
        value={`${x.vm.analytics.people_per_vacancy} чел. на вакансию`}
      />
      <Card
        title="Диапазон ожиданий по ЗП"
        withRubles
        value={`${x.vm.analytics.candidates_salary.start} – ${x.vm.analytics.candidates_salary.end}`}
      />
      <Card
        title="Медиальное значение по ожидаемой ЗП"
        withRubles
        value={`${x.vm.analytics.candidate_median_salary}`}
      />
    </div>
  );
});
