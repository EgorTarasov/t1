import { VacancyDto } from "@/api/models/vacancy.model";
import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { Column, DataTable } from "@/components/ui/data-table";
import { VacancyStore } from "@/stores/vacancy.store";
import { Priority } from "@/types/priority.type";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { observer } from "mobx-react-lite";

// название, рекуртер, дата создания, до дедлайна, приоритет
const columns: Column<VacancyDto.Item>[] = [
  {
    header: "Название",
    accessor: (item) => item.name,
  },
  {
    header: "Приоритет",
    accessor: (item) => Priority.locale[item.priority],
  },
  {
    header: "Дата создания",
    accessor: (item) => new Date(item.deadline).toLocaleDateString(),
  },
  {
    header: "До дедлайна",
    accessor: (item) => new Date(item.deadline).toLocaleDateString(),
  },
];

const Page = observer(() => {
  const vm = Route.useLoaderData();
  const navigate = useNavigate();

  return (
    <MainLayout title="Все вакансии">
      <DataTable data={vm.items} columns={columns} />
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/")({
  component: Page,
  loader: () => {
    checkAuth();
    return new VacancyStore();
  },
});
