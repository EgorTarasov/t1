import { VacancyStore } from "@/stores/vanacy.store";
import { FCVM } from "@/utils/vm";
import { observer } from "mobx-react-lite";
import { useEffect } from "react";
import { ChartSection } from "./chart-section";
import { Column, DataTable } from "@/components/ui/data-table";
import { CandidatesDto } from "@/api/models/candidates.model";

const activeColumns: Column<CandidatesDto.ActiveCandidate>[] = [
  {
    header: "№ кандидата",
    accessor: (x) => x.candidate_id,
  },
  {
    header: "Дата отклика",
    accessor: (x) => new Date(x.date_of_accept).toLocaleDateString("ru-RU"),
  },
  {
    header: "Статус",
    accessor: (x) => x.stage_name,
  },
  {
    header: "Источник",
    accessor: (x) => x.source,
  },
  {
    header: "% схожести\nс вакансией",
    accessor: (x) => `${x.similarity}%`,
  },
  {
    header: "Резюме",
    accessor: (x) => (
      <a
        href={"https://google.com"}
        target="_blank"
        rel="noreferrer"
        className="text-blue-500 underline"
      >
        Файл
      </a>
    ),
  },
];

const declinedColumns: Column<CandidatesDto.DeclinedCandidate>[] = [
  {
    header: "№ кандидата",
    accessor: (x) => x.candidate_id,
  },
  {
    header: "Дата отказа",
    accessor: (x) => new Date(x.date_of_decline).toLocaleDateString("ru-RU"),
  },
  {
    header: "Причина",
    accessor: (x) => x.reason,
  },
  {
    header: "Источник",
    accessor: (x) => x.source,
  },
  {
    header: "% схожести\nс вакансией",
    accessor: (x) => `${x.similarity}%`,
  },
  {
    header: "Резюме",
    accessor: (x) => (
      <a
        href={"https://google.com"}
        target="_blank"
        rel="noreferrer"
        className="text-blue-500 underline"
      >
        Файл
      </a>
    ),
  },
];

const potentialColumns: Column<CandidatesDto.PotentialCandidate>[] = [
  {
    header: "Источник",
    accessor: (x) => x.source,
    className: "w-[1%]",
  },
  {
    header: "% схожести\nс вакансией",
    accessor: (x) => `${x.similarity}%`,
  },
];

export const CandidatesView: FCVM<VacancyStore> = observer((x) => {
  useEffect(() => {
    x.vm.loadCandidates();
  }, [x.vm]);

  return (
    <div className="flex flex-col gap-4">
      <ChartSection title="Кандидаты по вакансии">
        {x.vm.activeCandidates && (
          <DataTable data={x.vm.activeCandidates} columns={activeColumns} />
        )}
      </ChartSection>
      <ChartSection title="Кандидаты с отказами">
        {x.vm.declinedCandidates && (
          <DataTable data={x.vm.declinedCandidates} columns={declinedColumns} />
        )}
      </ChartSection>
      <ChartSection title="Потенциальные кандидаты">
        {x.vm.potentialCandidates && (
          <DataTable
            data={x.vm.potentialCandidates}
            columns={potentialColumns}
          />
        )}
      </ChartSection>
    </div>
  );
});
