import { ThemeProvider, useTheme } from "@/components/hoc/theme-provider";
import { LoadingWrapper } from "@/components/ui/loaders/LoadingWrapper";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFoundPage from "@/pages/not-found.page";
import { Outlet, createRootRoute } from "@tanstack/react-router";
import React from "react";

const Toaster = React.lazy(() =>
  import("@/components/ui/sonner").then((m) => ({ default: m.Toaster })),
);

const Page = () => {
  const theme = useTheme();

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
        <Toaster richColors />
      </React.Suspense>
    </TooltipProvider>
  );
};

export const Route = createRootRoute({
  component: Page,
  pendingComponent: LoadingWrapper,
  notFoundComponent: NotFoundPage,
  // beforeLoad: () => AuthService.waitInit(),
});
