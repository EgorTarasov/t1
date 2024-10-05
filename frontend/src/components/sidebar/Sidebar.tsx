import { AnimatePresence, motion } from "framer-motion";
import { observer } from "mobx-react-lite";
import { Logo } from "../ui/logo";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { Link, useMatches } from "@tanstack/react-router";
import { RouteType } from "@/types/router.type";
import {
  BriefcaseIcon,
  CheckSquareIcon,
  PlusIcon,
  StarIcon,
  UsersIcon,
} from "lucide-react";
import { cn } from "@/utils/cn";
import { AuthState } from "./AuthState";
import { Button } from "../ui/button";

const transitionProps = {
  initial: { opacity: 0, translateX: -20 },
  animate: { opacity: 1, translateX: 0 },
  exit: { opacity: 0, translateX: -20 },
};

const items: {
  to: RouteType;
  label: string;
  icon: React.ElementType;
}[] = [
  {
    to: "/",
    label: "Вакансии",
    icon: BriefcaseIcon,
  },
  {
    to: "/login",
    label: "Мои задачи",
    icon: CheckSquareIcon,
  },
  {
    to: "/login",
    label: "Мои кандидаты",
    icon: UsersIcon,
  },
  {
    to: "/login",
    label: "Качество подбора",
    icon: StarIcon,
  },
];

const authRoutes: RouteType[] = ["/login", "/register"];

export const Sidebar = observer(() => {
  const matches = useMatches();
  const hideSidebar = matches.some((d) =>
    authRoutes.includes(d.pathname as RouteType),
  );

  return (
    <AnimatePresence mode="popLayout" initial={false}>
      {!hideSidebar && (
        <motion.aside
          key="sidebar"
          {...transitionProps}
          className="h-full w-64 bg-white shadow-md"
        >
          <ScrollArea className="flex-1 h-full overflow-auto py-4">
            <Link to="/" className="block px-6 py-5">
              <Logo />
            </Link>
            <ul className="flex flex-col gap-1 px-2">
              {items.map((item, i) => (
                <li key={i}>
                  <Link
                    to={item.to}
                    className={cn(
                      "font-medium flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 rounded-md",
                      "[&.active]:text-primary",
                    )}
                  >
                    <item.icon className="size-4" />
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
            <div className="mx-6 my-5">
              <Button className="w-full gap-1">
                <PlusIcon className="size-5" />
                Создать вакансию
              </Button>
            </div>
            <AuthState />
          </ScrollArea>
        </motion.aside>
      )}
    </AnimatePresence>
  );
});
