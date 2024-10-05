import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_base/vacancies")({
  component: () => <div>Hello /_base/vanacies!</div>,
  loader: checkAuth,
});
