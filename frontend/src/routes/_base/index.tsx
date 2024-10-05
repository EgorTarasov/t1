import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_base/")({
  component: () => <div>Hello /_base/!</div>,
  loader: checkAuth,
});
