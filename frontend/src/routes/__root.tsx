import { LoadingWrapper } from "@/components/ui/loaders/LoadingWrapper";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFoundPage from "@/pages/not-found.page";
import { Outlet, createRootRoute } from "@tanstack/react-router";
import React from "react";
import "@fontsource-variable/inter";
import { AuthService } from "@/stores/auth.service";

const Toaster = React.lazy(() =>
  import("@/components/ui/sonner").then((m) => ({ default: m.Toaster })),
);

const Page = () => {
  return (
    <TooltipProvider>
      <React.Suspense
        fallback={
          <div className="absolute inset-0 flex justify-center items-center">
            <LoadingWrapper />
          </div>
        }
      >
        <Outlet />
        <Toaster richColors theme="light" />
      </React.Suspense>
    </TooltipProvider>
  );
};

export const Route = createRootRoute({
  component: Page,
  pendingComponent: LoadingWrapper,
  notFoundComponent: NotFoundPage,
  beforeLoad: () => AuthService.waitInit(),
});
