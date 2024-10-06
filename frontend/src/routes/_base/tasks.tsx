import { TasksEndpoint } from "@/api/endpoints/tasks.endpoint";
import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { RejectCandidate } from "@/components/pages/tasks/reject-candidate";
import { Button } from "@/components/ui/button";
import { Column, DataTable } from "@/components/ui/data-table";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";
import { CheckIcon, UserXIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { useCallback, useMemo } from "react";

interface Task {
  id: number;
  stage: string;
  candidate_number: number;
  vacancy_name: string;
  deadline: string;
  resume_link: string;
}

const Page = observer(() => {
  const { tasks } = Route.useLoaderData();

  const onReject = useCallback((task: Task) => {
    console.log(task);
  }, []);

  const columns = useMemo<Column<Task>[]>(
    () => [
      {
        header: "Этап",
        accessor: (v) => (
          <div className="flex items-center text-nowrap gap-1">
            <button className="border rounded-md size-6 flex items-center justify-center group">
              <CheckIcon className="size-4 group-hover:opacity-100 opacity-0" />
            </button>
            {v.stage}
          </div>
        ),
      },
      {
        header: "№",
        accessor: (v) => v.candidate_number,
      },
      {
        header: "Вакансия",
        accessor: (v) => v.vacancy_name,
      },
      {
        header: "До дедлайна",
        accessor: (v) => {
          const deadline = new Date(v.deadline);
          const now = new Date();
          const diff = deadline.getTime() - now.getTime();
          const days = Math.ceil(diff / (1000 * 3600 * 24));
          return `${days} дн.`;
        },
      },
      {
        header: "Резюме",
        accessor: (v) => (
          <a
            href={v.resume_link}
            target="_blank"
            rel="noreferrer"
            className="text-blue-500 underline hover:no-underline"
          >
            Файл
          </a>
        ),
      },
      {
        header: <UserXIcon className="size-5" />,
        accessor: (v) => <RejectCandidate onReject={() => onReject(v)} />,
      },
    ],
    [onReject],
  );

  return (
    <MainLayout
      header={
        <div className="space-y-6">
          <h1 className="text-3xl font-semibold">Мои задачи</h1>
        </div>
      }
    >
      <DataTable data={tasks} columns={columns} />
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/tasks")({
  component: Page,
  beforeLoad: checkAuth,
  loader: async () => {
    // const tasks = await TasksEndpoint.list();
    const tasks: Task[] = [
      {
        id: 1,
        stage: "HR Скрининг",
        candidate_number: 1,
        vacancy_name: "vacancy",
        deadline: "2024-10-06T11:27:41.106023",
        resume_link: "https://google.com",
      },
    ];
    return { tasks };
  },
});
