import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";

const Page = () => {
  return (
    <MainLayout>
      <div className="flex items-center h-[200vh]">Hello /_base/!</div>
    </MainLayout>
  );
};

export const Route = createFileRoute("/_base/")({
  component: Page,
  loader: checkAuth,
});
