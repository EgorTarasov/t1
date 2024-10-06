import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";
import { observer } from "mobx-react-lite";

const Page = observer(() => {
  return (
    <MainLayout
      header={
        <div className="space-y-6">
          <h1 className="text-3xl font-semibold">Мои задачи</h1>
          <div className="flex flex-col">test</div>
        </div>
      }
    >
      test
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/tasks")({
  component: Page,
  beforeLoad: checkAuth,
  loader: async (x) => {},
});
