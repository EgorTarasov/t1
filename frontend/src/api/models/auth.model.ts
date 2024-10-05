import { z } from "zod";

export namespace AuthDto {
  export const Token = z.object({
    access_token: z.string(),
  });

  export const User = z.object({
    first_name: z.string(),
    last_name: z.string(),
    email: z.string(),
  });
}
