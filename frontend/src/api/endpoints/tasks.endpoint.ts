import { z } from "zod";
import { SkillDto } from "../models/skill.model";
import api from "../utils/api";
import { TaskDto } from "../models/task.model";

export namespace TasksEndpoint {
  export const list = () => {
    return api.get("/vacancies/recruiter/stages", {
      schema: z.array(TaskDto.Item),
    });
  };
}
