import { routeTree } from "@/routeTree.gen";
import { ParseRoute } from "@tanstack/react-router";

export type RouteType = ParseRoute<typeof routeTree>["fullPath"];
