import api from "api/utils/api";
import { AuthDto } from "../models/auth.model";

export namespace AuthEndpoint {
  export interface LoginTemplate {
    email: string;
    password: string;
  }
  export const login = async (v: LoginTemplate) =>
    api.post("/users/login", v, {
      schema: AuthDto.Token,
    });

  export interface RegisterTemplate {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
  }
  export const register = async (v: RegisterTemplate) =>
    api.post("/users/register", v, {
      schema: AuthDto.Token,
    });

  export const test = async () => {
    api.get("/user");
  };
}
