import { z } from "zod";
import { SkillDto } from "../models/skill.model";
import api from "../utils/api";

export namespace SkillEndpoint {
  export const list = () => {
    return api.get("/vacancies/skills/all", {
      schema: z.array(SkillDto.Item),
    });
  };

  export const create = (names: string[]) => {
    return api.post(
      "/vacancies/skills/new",
      names.map((name) => ({ name })),
      {
        schema: z.array(SkillDto.Item),
      },
    );
  };
}
