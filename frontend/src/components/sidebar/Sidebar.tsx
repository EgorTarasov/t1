import { AnimatePresence, motion } from "framer-motion";
import { observer } from "mobx-react-lite";
import { Logo } from "../ui/logo";
import {
  Link,
  useLocation,
  useMatches,
  useNavigate,
} from "@tanstack/react-router";
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
  active?: (v: string) => boolean;
  disabled?: boolean;
}[] = [
  {
    to: "/",
    label: "Вакансии",
    icon: BriefcaseIcon,
    active: (pathname) =>
      pathname.includes("/vacancy") && !pathname.includes("/vacancy/new"),
  },
  {
    to: "/tasks",
    label: "Мои задачи",
    icon: CheckSquareIcon,
  },
  {
    to: "/login",
    label: "Мои кандидаты",
    icon: UsersIcon,
    disabled: true,
  },
  {
    to: "/login",
    label: "Качество подбора",
    icon: StarIcon,
    disabled: true,
  },
];

export const Sidebar: FC<{ hideSidebar?: boolean }> = observer(
  ({ hideSidebar }) => {
    const { pathname } = useLocation();
    const navigate = useNavigate();

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
                      disabled={item.disabled}
                      className={cn(
                        item.active?.(pathname) && "active",
                        "font-medium flex items-center gap-2 px-4 py-2 text-sm text-slate-700 rounded-md",
                        !item.disabled && "hover:bg-slate-100",
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
                <Button
                  onClick={() => {
                    navigate({ to: "/vacancy/new" });
                  }}
                  className={"w-full gap-1"}
                  disabled={pathname.includes("/vacancy/new")}
                >
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
  },
);
