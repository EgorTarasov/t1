import { AuthDto } from "@/api/models/auth.model";
import { z } from "zod";

export namespace Auth {
  export interface Authenticated {
    state: "authenticated";
    user: z.infer<typeof AuthDto.User>;
  }

  export interface Anonymous {
    state: "anonymous";
  }

  export interface Loading {
    state: "loading";
  }

  export type State = Authenticated | Anonymous | Loading;
}
