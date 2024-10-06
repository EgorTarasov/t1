import { z } from "zod";
import { Priority } from "@/types/priority.type";
import { SkillDto } from "./skill.model";

export namespace VacancyDto {
  const SourceSchema = z.object({
    name: z.string(),
    count: z.number(),
  });

  const DeclineReasonSchema = z.object({
    reason: z.string(),
    count: z.number(),
  });

  const StageSchema = z.object({
    id: z.number(),
    name: z.string(),
    order: z.number(),
    success_rate: z.number(),
    avg_duration: z.number(),
    max_duration: z.number(),
    number_of_candidates: z.number(),
    sources: z.array(SourceSchema),
    decline_reasons: z.array(DeclineReasonSchema),
  });

  export const Item = z.object({
    id: z.number(),
    name: z.string(),
    priority: Priority.Schema,
    deadline: z.string(),
    profession: z.string(),
    area: z.string(),
    supervisor: z.string(),
    city: z.string(),
    experience_from: z.number(),
    experience_to: z.number(),
    education: z.string(),
    quantity: z.number(),
    description: z.string(),
    type_of_employment: z.string(),
    vacancy_skills: z.array(SkillDto.Item),
    // additional_skills: z.array(z.any()),
    recruiter: z.null(),
    hr: z.null(),
    created_at: z.string(),
  });
  export type Item = z.infer<typeof Item>;

  export const DetailedItem = z.object({
    vacancy: Item,
    stages: z.array(StageSchema),
  });
  export type DetailedItem = z.infer<typeof DetailedItem>;
}

export const mockVacancy: VacancyDto.DetailedItem = {
  vacancy: {
    id: 1,
    name: "Разработчик",
    priority: 1,
    deadline: "2025-01-01T00:00:00",
    profession: "Программист",
    area: "Разработка",
    supervisor: "Иванов Иван Иванович",
    city: "Москва",
    experience_from: 3,
    experience_to: 6,
    education: "Высшее",
    quantity: 1,
    description: "Разработчик",
    type_of_employment: "Полная занятость",
    vacancy_skills: [
      {
        id: 1,
        name: "JavaScript",
      },
      {
        id: 2,
        name: "TypeScript",
      },
    ],
    recruiter: null,
    hr: null,
    created_at: "2021-01-01T00:00:00",
  },
  stages: [
    {
      id: 1,
      name: "Hr скриннинг",
      order: 1,
      success_rate: 0.7, // 100%
      avg_duration: 2, // 2 / 20
      max_duration: 20,
      number_of_candidates: 100, // 100
      sources: [
        {
          name: "hh.ru",
          count: 50,
        },
        {
          name: "linkedin",
          count: 50,
        },
      ],
      decline_reasons: [
        {
          reason: "Не подходит",
          count: 50,
        },
        {
          reason: "Не отвечает",
          count: 50,
        },
      ],
    },
    {
      id: 2,
      name: "Телефонное интервью",
      order: 2,
      success_rate: 0.5,
      avg_duration: 3,
      max_duration: 15,
      number_of_candidates: 50,
      sources: [
        {
          name: "hh.ru",
          count: 25,
        },
        {
          name: "linkedin",
          count: 25,
        },
      ],
      decline_reasons: [
        {
          reason: "Не подходит",
          count: 25,
        },
        {
          reason: "Не отвечает",
          count: 25,
        },
      ],
    },
    {
      id: 3,
      name: "Финальное интервью",
      order: 3,
      success_rate: 0.3,
      avg_duration: 5,
      max_duration: 10,
      number_of_candidates: 20,
      sources: [
        {
          name: "hh.ru",
          count: 10,
        },
        {
          name: "linkedin",
          count: 10,
        },
      ],
      decline_reasons: [
        {
          reason: "Не подходит",
          count: 10,
        },
        {
          reason: "Не отвечает",
          count: 10,
        },
      ],
    },
    {
      id: 4,
      name: "Получение оффера",
      order: 4,
      success_rate: 0.9,
      avg_duration: 1,
      max_duration: 5,
      number_of_candidates: 5,
      sources: [
        {
          name: "hh.ru",
          count: 3,
        },
        {
          name: "linkedin",
          count: 2,
        },
      ],
      decline_reasons: [
        {
          reason: "Не подходит",
          count: 3,
        },
        {
          reason: "Не отвечает",
          count: 2,
        },
      ],
    },
    {
      id: 5,
      name: "выходит в штат",
      order: 5,
      success_rate: 1,
      avg_duration: 0,
      max_duration: 0,
      number_of_candidates: 5,
      sources: [
        {
          name: "hh.ru",
          count: 3,
        },
        {
          name: "linkedin",
          count: 2,
        },
      ],
      decline_reasons: [
        {
          reason: "Не подходит",
          count: 0,
        },
        {
          reason: "Не отвечает",
          count: 0,
        },
      ],
    },
  ],
};
