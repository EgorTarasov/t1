import { redirect } from "@tanstack/react-router";

export const checkGrant = (allowed: boolean) => {
  if (allowed) {
    return;
  }

  throw new Error("You shall not pass! (implement redirect)");
  // throw redirect({
  //   to: "/",
  // });
};
