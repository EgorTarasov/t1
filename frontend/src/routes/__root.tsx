import { ThemeProvider } from "@/components/hoc/theme-provider";
import NotFoundPage from "@/components/pages/not-found.page";
import { LoadingWrapper } from "@/components/ui/loaders/LoadingWrapper";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Outlet, createRootRoute } from "@tanstack/react-router";
import React from "react";

const Toaster = React.lazy(() =>
  import("@/components/ui/sonner").then((m) => ({ default: m.Toaster })),
);

const Page = () => {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
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
    </ThemeProvider>
  );
};

export const Route = createRootRoute({
  component: Page,
  pendingComponent: LoadingWrapper,
  notFoundComponent: NotFoundPage,
  // beforeLoad: () => AuthService.waitInit(),
});
