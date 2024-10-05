import { ScrollArea } from "@/components/ui/scroll-area";
import { observer } from "mobx-react-lite";
import { FC, PropsWithChildren } from "react";

interface Props extends PropsWithChildren {
  title: string;
}

export const MainLayout: FC<Props> = observer((x) => {
  return (
    <main className="size-full grid grid-rows-[auto_1fr] py-10 gap-6 px-8 mx-auto 2xl:ml-8 max-w-screen-xl">
      <h1 className="text-3xl font-semibold text-slate-900">{x.title}</h1>
      <ScrollArea className="flex flex-col h-full">{x.children}</ScrollArea>
    </main>
  );
});
