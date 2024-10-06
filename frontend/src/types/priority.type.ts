import { z } from "zod";

export namespace Priority {
  export enum Priority {
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3,
  }

  export const Schema = z.nativeEnum(Priority);

  export const locale = {
    [Priority.LOW]: "Низкий",
    [Priority.MEDIUM]: "Средний",
    [Priority.HIGH]: "Высокий",
  };
}
