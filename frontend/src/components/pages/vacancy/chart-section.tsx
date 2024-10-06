import { Button } from "@/components/ui/button";
import { cn } from "@/utils/cn";
import { ChevronDownIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC, PropsWithChildren, useState } from "react";

interface Props extends PropsWithChildren {
  title: string;
  description?: string;
  collapsible?: boolean;
  allowOverflow?: boolean;
}

export const ChartSection: FC<Props> = observer(
  ({ collapsible = true, ...x }) => {
    const [collapsed, setCollapsed] = useState(false);

    return (
      <section className="bg-white rounded-2xl border w-full">
        <div className="flex justify-between p-5 pb-0">
          <h2
            className={cn(
              "text-2xl font-medium",
              collapsible && "text-slate-500",
            )}
          >
            {x.title}
          </h2>
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
        {!collapsed && x.description && (
          <p className="text-sm mt-2 px-5">{x.description}</p>
        )}
        <div
          className={cn(
            "flex gap-8 xl:gap-32 mt-3 overflow-auto p-5 pt-0",
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
