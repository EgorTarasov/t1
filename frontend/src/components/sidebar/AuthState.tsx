import { AuthService } from "@/stores/auth.service";
import { LogOutIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { FC } from "react";

export const AuthState = observer((x) => {
  if (AuthService.auth.state !== "authenticated") return null;

  const user = AuthService.auth.user;
  return (
    <div className="px-6 flex items-center justify-between">
      <div className="pl-1">
        <p className="text-sm font-medium">
          {user.first_name} {user.last_name}
        </p>
        <p className="text-xs text-slate-400">{user.email}</p>
      </div>
      <button
        onClick={() => AuthService.logout()}
        className="text-slate-400 p-2 rounded-md hover:bg-slate-100"
      >
        <LogOutIcon className="size-5" />
      </button>
    </div>
  );
});
