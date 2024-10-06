import { Button } from "@/components/ui/button";
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
import { Textarea } from "@/components/ui/textarea";
import { observer } from "mobx-react-lite";
import { FC, useState } from "react";

interface Props {
  onReject: (reason: string) => void;
}

export const RejectCandidate: FC<Props> = observer((x) => {
  const [reason, setReason] = useState("");

  return (
    <Dialog>
      <DialogTrigger className="text-red-500 underline hover:no-underline">
        Отказ
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Отказ</DialogTitle>
          <DialogDescription>Укажите причину отказа</DialogDescription>
        </DialogHeader>
        <Textarea
          placeholder="Отказался от предложения"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />
        <DialogFooter>
          <DialogClose asChild>
            <Button
              variant="destructive"
              disabled={!reason}
              onClick={() => {
                x.onReject(reason);
                setReason("");
              }}
            >
              Отказать
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
});
