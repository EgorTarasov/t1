import api from "api/utils/api";
import { AuthDto } from "../models/auth.model";

export namespace AuthEndpoint {
  export interface LoginTemplate {
    email: string;
    password: string;
  }
  export const login = async (v: LoginTemplate) =>
    api.post("/auth/email/login", v, {
      schema: AuthDto.Token,
    });

  export interface RegisterTemplate {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }
  export const register = async (v: RegisterTemplate) =>
    api.post("/auth/email/register", v, {
      schema: AuthDto.Token,
    });

  export const me = async () =>
    api.get("/auth/me", {
      schema: AuthDto.User,
    });
}
