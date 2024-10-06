import { VacancyEndpoint } from "@/api/endpoints/vacanvy.endpoint";
import { SkillDto } from "@/api/models/skill.model";
import { Priority } from "@/types/priority.type";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable } from "mobx";

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

  async create() {
    const vacancy = await VacancyEndpoint.create({
      name: this.name,
      priority: this.priority,
      deadline: this.deadline,
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
      // stages: this.stages.map((x) => ({
      //   name: x.name,
      //   sla: x.sla,
      // })),
    });
    return vacancy;
  }

  dispose(): void {}
}
