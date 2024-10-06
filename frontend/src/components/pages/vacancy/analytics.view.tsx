import { LoadingWrapper } from "@/components/ui/loaders/LoadingWrapper";
import { VacancyStore } from "@/stores/vanacy.store";
import { cn } from "@/utils/cn";
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
  className?: string;
}> = observer((x) => {
  return (
    <div
      className={cn(
        "font-medium rounded-xl p-4 flex flex-col gap-2 bg-white",
        x.className,
      )}
    >
      <div className="flex items-center">
        <h3 className="text-xl">{x.value}</h3>
        {x.withRubles && (
          <RussianRubleIcon className="size-4" strokeWidth={2.5} />
        )}
      </div>
      <p className="text-nowrap">{x.title}</p>
    </div>
  );
});

export const AnalyticsView: FC<Props> = observer((x) => {
  useEffect(() => {
    x.vm.fetchAnalytics();
  }, [x.vm]);

  if (!x.vm.analytics) return <LoadingWrapper />;

  const getColorClass = (
    salary: number,
    market: { start: number; end: number },
  ) => {
    if (salary < market.start) {
      return "bg-red-200";
    } else if (salary > market.end) {
      return "bg-orange-200";
    } else {
      return "bg-green-200";
    }
  };

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
        className={getColorClass(
          x.vm.analytics.candidate_median_salary,
          x.vm.analytics.market_salary,
        )}
      />
    </div>
  );
});
