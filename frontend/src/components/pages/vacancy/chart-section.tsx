import { Button } from "@/components/ui/button";
import { cn } from "@/utils/cn";
import { ReactNode } from "@tanstack/react-router";
import { ChevronDownIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC, PropsWithChildren, useState } from "react";

interface Props extends PropsWithChildren {
  title: string;
  description?: string;
  collapsible?: boolean;
  actions?: ReactNode;
  allowOverflow?: boolean;
}

export const ChartSection: FC<Props> = observer(
  ({ collapsible = true, ...x }) => {
    const [collapsed, setCollapsed] = useState(false);

    return (
      <section className="bg-white rounded-2xl border w-full py-5">
        <div className="grid-cols-[auto_auto] grid-flow-dense grid lg:flex justify-between px-5 pb-0 items-center gap-1">
          <h2
            className={cn(
              "text-2xl font-medium",
              collapsible && "text-slate-500",
            )}
          >
            {x.title}
          </h2>
          {x.actions && (
            <div className="col-span-2 ml-auto">{!collapsed && x.actions}</div>
          )}
          <div className="flex items-center gap-1">
            {collapsible && (
              <Button
                variant="ghost"
                size="icon"
                className={cn(
                  "size-8 flex items-center justify-center",
                  !collapsed && "rotate-180",
                )}
                onClick={() => setCollapsed(!collapsed)}
              >
                <ChevronDownIcon className="siz-6" />
              </Button>
            )}
          </div>
        </div>
        {!collapsed && x.description && (
          <p className="text-sm mt-2 px-5">{x.description}</p>
        )}
        <div
          className={cn(
            "flex flex-col md:flex-row gap-8 xl:gap-32 mt-3 overflow-auto px-5",
            collapsed && "hidden",
            x.allowOverflow && "overflow-visible",
          )}
        >
          {x.children}
        </div>
      </section>
    );
  },
);
