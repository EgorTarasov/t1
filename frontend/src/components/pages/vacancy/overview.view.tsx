import { VacancyStore } from "@/stores/vanacy.store";
import { cn } from "@/utils/cn";
import { observer } from "mobx-react-lite";
import { FC } from "react";

interface Props {
  vm: VacancyStore;
}

const LabelValue: FC<{ label: string; value: string; row?: boolean }> = ({
  label,
  value,
  row = false,
}) => {
  return (
    <div
      className={cn(
        "space-y-2 text-sm",
        row ? "flex items-center gap-2 space-y-0" : "",
      )}
    >
      <div className="font-semibold">{label}:</div>
      <div>{value}</div>
    </div>
  );
};

const LabelList: FC<{ label: string; values: string[] }> = ({
  label,
  values,
}) => {
  return (
    <div className="space-y-3 pt-2">
      <h2 className="text-xl font-medium">{label}</h2>
      <ul className="flex flex-wrap gap-2">
        {values.map((x) => (
          <li
            key={x}
            className="bg-slate-200 rounded-md px-3 py-1 text-slate-500"
          >
            {x}
          </li>
        ))}
      </ul>
    </div>
  );
};

export const OverviewView: FC<Props> = observer((x) => {
  return (
    <div className="space-y-4 pt-8">
      <div className="space-y-4 bg-white p-4 rounded-xl">
        <h2 className="text-xl font-medium">Основная информация</h2>
        <div className="flex gap-8 flex-wrap">
          <LabelValue
            label="Руководитель"
            value={x.vm.vacancy.vacancy.supervisor}
          />
          <LabelValue label="Город" value={x.vm.vacancy.vacancy.city} />
          <LabelValue
            label="Режим работы"
            value={x.vm.vacancy.vacancy.type_of_employment}
          />
        </div>
        <LabelValue label="Описание" value={x.vm.vacancy.vacancy.description} />
        <LabelList
          label="Источники размещения вакансии"
          values={x.vm.vacancy.stages[0].sources.map((x) => x.name)}
        />
      </div>
      <div className="space-y-4 bg-white p-4 rounded-xl">
        <h2 className="text-xl font-medium">Требования к кандидату</h2>
        <LabelValue
          row
          label="Опыт работы"
          value={`${x.vm.vacancy.vacancy.experience_from} – ${x.vm.vacancy.vacancy.experience_to} лет`}
        />
        <LabelValue
          row
          label="Образование"
          value={x.vm.vacancy.vacancy.education}
        />
        <LabelList
          label="Ключевые навыки"
          values={x.vm.vacancy.vacancy.vacancy_skills.map((x) => x.name)}
        />
      </div>
    </div>
  );
});
