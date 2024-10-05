import { Sidebar } from "@/components/sidebar/Sidebar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RouteType } from "@/types/router.type";
import {
  createLazyFileRoute,
  useMatch,
  useMatches,
} from "@tanstack/react-router";
import React from "react";

const AnimatedOutlet = React.lazy(() =>
  import("@/components/router/animated-outlet").then((m) => ({
    default: m.AnimatedOutlet,
  })),
);

const AnimatePresence = React.lazy(() =>
  import("framer-motion").then((m) => ({ default: m.AnimatePresence })),
);

const authRoutes: RouteType[] = ["/login", "/register"];

const Page = () => {
  const matches = useMatches();
  const match = useMatch({ strict: false });
  const nextMatchIndex = matches.findIndex((d) => d.id === match.id) + 1;
  const nextMatch = matches[nextMatchIndex];

  const hideSidebar = matches.some((d) =>
    authRoutes.includes(d.pathname as RouteType),
  );

  return (
    <>
      <Sidebar hideSidebar={hideSidebar} />
      <AnimatePresence mode="popLayout">
        <AnimatedOutlet key={nextMatch.id} />
      </AnimatePresence>
    </>
  );
};

export const Route = createLazyFileRoute("/_base")({
  component: Page,
});
