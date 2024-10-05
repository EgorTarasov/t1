import { observer } from "mobx-react-lite";
import { FC, PropsWithChildren } from "react";

interface Props extends PropsWithChildren {
  title: string;
  description: string;
}

export const ChartSection: FC<Props> = observer((x) => {
  return (
    <section className="bg-white p-5 rounded-2xl border overflow-hidden w-full">
      <h2 className="text-2xl font-medium text-slate-500">{x.title}</h2>
      <p className="text-sm mt-2">{x.description}</p>
      <div className="flex gap-8 xl:gap-32 mt-3 overflow-auto">
        {x.children}
      </div>
    </section>
  );
});
