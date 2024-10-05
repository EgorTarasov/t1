import { ScrollArea } from "@/components/ui/scroll-area";
import { observer } from "mobx-react-lite";
import { FC, PropsWithChildren } from "react";

type Props = PropsWithChildren;

export const MainLayout: FC<Props> = observer((x) => {
  return (
    <main className="size-full">
      <ScrollArea className="flex flex-col h-full">{x.children}</ScrollArea>
    </main>
  );
});
