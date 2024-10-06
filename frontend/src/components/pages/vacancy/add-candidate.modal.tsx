import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button, buttonVariants } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC } from "react";
import { IconInput } from "@/components/ui/input";

interface Props {
  onSubmit: (candidate: { source: string; resumeLink: string }) => void;
}

export const AddCandidateModal: FC<Props> = observer((x) => {
  return (
    <Dialog>
      <DialogTrigger
        className={buttonVariants({ variant: "outline", size: "sm" })}
      >
        <>
          <PlusIcon className="size-4" />
          Добавить кандидата
        </>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Добавить кандидата</DialogTitle>
          <DialogDescription>Укажите данные кандидата</DialogDescription>
        </DialogHeader>
        <IconInput
          id="source"
          label="Источник"
          placeholder="Например, LinkedIn"
        />
        <IconInput
          id="resumeLink"
          label="Ссылка на резюме"
          placeholder="Например, https://linkedin.com/in/username"
        />
        <DialogFooter>
          <DialogClose asChild>
            <Button>Добавить</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
});
