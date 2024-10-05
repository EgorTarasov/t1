import { AuthService } from "@/stores/auth.service";
import { redirect } from "@tanstack/react-router";

export const checkAuth = () => {
  console.log("check");
  if (AuthService.auth.state === "authenticated") {
    return;
  }

  throw redirect({
    to: "/login",
  });
};
