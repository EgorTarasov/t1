import { AnimatePresence, motion } from "framer-motion";
import { observer } from "mobx-react-lite";
import { Logo } from "../ui/logo";
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
import { Button, buttonVariants } from "../ui/button";
import { FC } from "react";
import { ScrollArea } from "../ui/scroll-area";

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

export const Sidebar: FC<{ hideSidebar?: boolean }> = observer(
  ({ hideSidebar }) => {
    return (
      <AnimatePresence mode="popLayout" initial={false}>
        {!hideSidebar && (
          <motion.aside
            key="sidebar"
            {...transitionProps}
            className="h-full overflow-hidden w-64 bg-white shadow-md"
          >
            <ScrollArea className="py-4 h-full">
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
                <Link
                  to="/vacancy/new"
                  className={cn(buttonVariants(), "w-full gap-1")}
                >
                  <PlusIcon className="size-5" />
                  Создать вакансию
                </Link>
              </div>
              <AuthState />
            </ScrollArea>
          </motion.aside>
        )}
      </AnimatePresence>
    );
  },
);
