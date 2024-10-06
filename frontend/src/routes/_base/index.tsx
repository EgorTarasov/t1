import { VacancyDto } from "@/api/models/vacancy.model";
import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { Column, DataTable } from "@/components/ui/data-table";
import { IconInput } from "@/components/ui/input";
import { VacanciesStore } from "@/stores/vacancies.store";
import { Priority } from "@/types/priority.type";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { SearchIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { useState } from "react";

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
    accessor: (item) => new Date(item.created_at).toLocaleDateString("ru-RU"),
  },
  {
    header: "До дедлайна",
    accessor: (item) => new Date(item.deadline).toLocaleDateString("ru-RU"),
  },
];

const Page = observer(() => {
  const vm = Route.useLoaderData();
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  return (
    <MainLayout
      header={
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold text-slate-900">
            Все вакансии
          </h1>
          <IconInput
            placeholder="Поиск"
            value={search}
            leftIcon={<SearchIcon />}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      }
    >
      <DataTable
        data={vm.items.filter((x) =>
          x.name.toLowerCase().includes(search.toLowerCase()),
        )}
        columns={columns}
        onRowClick={(v) =>
          navigate({
            to: "/vacancy/$id",
            params: {
              id: v.id.toString(),
            },
          })
        }
      />
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/")({
  component: Page,
  beforeLoad: checkAuth,
  loader: async () => {
    checkAuth();

    const vm = new VacanciesStore();

    await vm.init();

    return vm;
  },
});
