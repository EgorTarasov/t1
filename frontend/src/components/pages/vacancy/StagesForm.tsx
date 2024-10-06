import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { NewVacancyStore } from "@/stores/new-vacancy";
import { PlusIcon, Trash2Icon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC } from "react";

interface Props {
  vm: NewVacancyStore;
}

export const StagesForm: FC<Props> = observer((x) => {
  return (
    <div className="col-span-2 w-full space-y-3">
      <h3 className="text-xl font-medium">Этапы отбора</h3>
      <div className="flex w-full gap-4">
        <div className="flex gap-2 flex-col flex-1">
          <Label>Название этапа</Label>
          {x.vm.stages.map((v) => (
            <div key={v.id}>
              <Input
                autoFocus
                className="bg-primary text-primary-foreground border-none font-medium"
                value={v.name}
                onChange={(e) => {
                  v.name = e.target.value;
                }}
              />
            </div>
          ))}
          <Button variant="secondary" size="sm" onClick={() => x.vm.addStage()}>
            <PlusIcon />
          </Button>
        </div>
        <div className="flex gap-2 flex-col sm:flex-1">
          <Label>SLA этапа в днях</Label>
          {x.vm.stages.map((v) => (
            <div key={v.id} className="flex items-center gap-2">
              <Input
                className="w-[100px]"
                value={v.sla}
                type="number"
                onChange={(e) => {
                  const number = Number(e.target.value);
                  if (!isNaN(number) && number >= 0) {
                    v.sla = number;
                  }
                }}
              />
              <Button
                size="icon"
                variant="ghost"
                onClick={() => x.vm.removeStage(v)}
              >
                <Trash2Icon className="size-5" />
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
});
