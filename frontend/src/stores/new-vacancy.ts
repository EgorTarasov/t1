import { VacancyEndpoint } from "@/api/endpoints/vacanvy.endpoint";
import { SkillDto } from "@/api/models/skill.model";
import { Priority } from "@/types/priority.type";
import { DisposableVm } from "@/utils/vm";
import { NavigateFn } from "@tanstack/react-router";
import { makeAutoObservable } from "mobx";
import { toast } from "sonner";

export class StageStore {
  name = "";
  sla = 0;
  readonly id = Math.random();

  constructor() {
    makeAutoObservable(this);
  }
}

export class NewVacancyStore implements DisposableVm {
  name = "";
  priority: Priority.Priority = Priority.Priority.LOW;
  deadline: Date = new Date();
  profession = "";
  area = "";
  supervisor = "";
  city = "";
  experienceFrom = "";
  experienceTo = "";
  education = "";
  keySkills: SkillDto.Item[] = [];
  additionalSkills: SkillDto.Item[] = [];
  description = "";
  typeOfEmployment = "";
  quantity = 1;
  direction = "";
  salaryLow = "";
  salaryHigh = "";

  loading = false;

  stages: StageStore[] = [];

  addStage() {
    this.stages.push(new StageStore());
  }

  removeStage(stage: StageStore) {
    this.stages = this.stages.filter((x) => x !== stage);
  }

  constructor() {
    makeAutoObservable(this);
  }

  validate(): boolean {
    if (this.name.length < 3) {
      toast.error("Название вакансии должно быть не менее 3 символов");
      return false;
    }

    if (Number(this.salaryLow) > Number(this.salaryHigh)) {
      toast.error("Минимальная зарплата не может быть больше максимальной");
      return false;
    }

    if (this.stages.length < 1) {
      toast.error("Необходимо добавить хотя бы один этап");
      return false;
    }

    if (this.keySkills.length < 1) {
      toast.error("Необходимо добавить хотя бы один ключевой навык");
      return false;
    }

    if (Number(this.experienceFrom) > Number(this.experienceTo)) {
      toast.error("Неверно указаны годы опыта");
      return false;
    }

    return true;
  }

  async create(navigate: NavigateFn) {
    const id = await VacancyEndpoint.create({
      name: this.name,
      priority: this.priority,
      deadline: this.deadline.toISOString().split("T")[0] + "T00:00:00",
      profession: this.profession,
      area: this.area,
      supervisor: this.supervisor,
      city: this.city,
      experienceFrom: this.experienceFrom,
      experienceTo: this.experienceTo,
      education: this.education,
      keySkills: this.keySkills.map((x) => x.id),
      additionalSkills: this.additionalSkills.map((x) => x.id),
      description: this.description,
      typeOfEmployment: this.typeOfEmployment,
      quantity: this.quantity,
      direction: this.direction,
      salary_low: Number(this.salaryLow),
      salary_high: Number(this.salaryHigh),
      stages: this.stages.map((x, i) => ({
        order: i + 1,
        name: x.name,
        duration: x.sla,
      })),
    });

    navigate({ to: "/vacancy/$id", params: { id: id.toString() } });

    return id;
  }

  dispose(): void {
    return;
  }
}
