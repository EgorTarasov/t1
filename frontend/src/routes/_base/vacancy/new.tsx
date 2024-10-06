import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { ChartSection } from "@/components/pages/vacancy/chart-section";
import { IconInput, Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Priority } from "@/types/priority.type";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute } from "@tanstack/react-router";
import { observer } from "mobx-react-lite";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { NewVacancyStore } from "@/stores/new-vacancy";
import { useViewModel } from "@/utils/vm";
import { SkillsDropdown } from "@/components/dropdowns/SkillsDropdown";
import { Textarea } from "@/components/ui/textarea";
import DropdownMultiple from "@/components/DropdownMultiple";
import { StagesForm } from "@/components/pages/vacancy/StagesForm";
import { Button } from "@/components/ui/button";

const Page = observer(() => {
  const vm = useViewModel(NewVacancyStore);

  return (
    <MainLayout title="Новая вакансия">
      <div className="space-y-4">
        <ChartSection
          title="Основная информация"
          collapsible={false}
          allowOverflow
        >
          <div className="flex flex-wrap gap-4">
            <IconInput
              id="title"
              className="w-[300px]"
              value={vm.name}
              onChange={(e) => {
                vm.name = e.target.value;
              }}
              label="Название вакансии"
              placeholder="Фронтенд разработчик"
            />
            <div>
              <Label htmlFor="priority">Приоритет</Label>
              <Select
                key={vm.priority}
                value={vm.priority.toString()}
                onValueChange={(value) => {
                  vm.priority = Number(value);
                }}
              >
                <SelectTrigger id="priority" className="w-[180px]">
                  <SelectValue placeholder="Выберите приоритет" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">{Priority.locale[1]}</SelectItem>
                  <SelectItem value="2">{Priority.locale[2]}</SelectItem>
                  <SelectItem value="3">{Priority.locale[3]}</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </ChartSection>
        <ChartSection
          title="Основная информация"
          collapsible={false}
          allowOverflow
        >
          <div className="flex flex-wrap gap-4">
            <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-x-1 h-fit">
              <Label
                htmlFor="experience_from"
                className="col-span-3 mt-1.5 mb-1"
              >
                Опыт работы, лет
              </Label>
              <IconInput
                id="experience_from"
                type="number"
                placeholder="от"
                value={vm.experienceFrom}
                onChange={(e) => {
                  const value = Number(e.target.value);
                  if (
                    value > Number(vm.experienceTo || 99) ||
                    value < 0 ||
                    value > 99
                  ) {
                    return;
                  }
                  vm.experienceFrom = e.target.value;
                }}
                className="w-24"
              />
              <span>–</span>
              <IconInput
                id="experience_to"
                type="number"
                placeholder="до"
                value={vm.experienceTo}
                onChange={(e) => {
                  const value = Number(e.target.value);
                  if (value > 99 || value < 0) {
                    return;
                  }
                  vm.experienceTo = e.target.value;
                }}
                className="w-24"
              />
            </div>
            <IconInput
              type="number"
              label="Кол-во мест"
              placeholder="1"
              value={vm.quantity}
              onChange={(e) => {
                const value = Number(e.target.value);
                if (value < 1 || value > 99) {
                  return;
                }
                vm.quantity = value;
              }}
              className="w-24"
            />
            <IconInput
              label="Образование"
              placeholder="Высшее"
              value={vm.education}
              onChange={(e) => {
                vm.education = e.target.value;
              }}
              className="w-[400px]"
            />
            <div className="w-full flex gap-4 *:w-[250px]">
              <SkillsDropdown
                label="Ключевые навыки"
                value={vm.keySkills}
                onChange={(value) => {
                  vm.keySkills = value;
                }}
                filter={(value) => !vm.additionalSkills.includes(value)}
              />
              <SkillsDropdown
                label="Дополнительные навыки"
                value={vm.additionalSkills}
                filter={(value) => !vm.keySkills.includes(value)}
                onChange={(value) => {
                  vm.additionalSkills = value;
                }}
              />
            </div>
          </div>
        </ChartSection>
        <ChartSection
          title="Подробности о вакансии"
          collapsible={false}
          allowOverflow
        >
          <div className="grid grid-cols-2 w-full gap-6 gap-x-4">
            <div>
              <Label htmlFor="description">Описание</Label>
              <Textarea
                id="description"
                placeholder="О чем вакансия?"
                value={vm.description}
                onChange={(e) => {
                  vm.description = e.target.value;
                }}
              />
            </div>
            <div className="grid grid-cols-2">
              <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-x-1 h-fit">
                <Label
                  htmlFor="experience_from"
                  className="col-span-3 mt-1.5 mb-1"
                >
                  Опыт работы, лет
                </Label>
                <IconInput
                  id="experience_from"
                  type="number"
                  placeholder="от"
                  onChange={(e) => {
                    const value = Number(e.target.value);
                    if (
                      value > Number(vm.experienceTo || 99) ||
                      value < 0 ||
                      value > 99
                    ) {
                      return;
                    }
                    vm.experienceFrom = e.target.value;
                  }}
                  className="w-24"
                />
                <span>–</span>
                <IconInput
                  id="experience_to"
                  type="number"
                  placeholder="до"
                  value={vm.experienceTo}
                  onChange={(e) => {
                    const value = Number(e.target.value);
                    if (value > 99 || value < 0) {
                      return;
                    }
                    vm.experienceTo = e.target.value;
                  }}
                  className="w-24"
                />
              </div>
            </div>
            {/* <DropdownMultiple
              label="График работы"
              value={vm.typeOfEmployment}
              onChange={(value) => {
                vm.typeOfEmployment = value;
              }}
              options={vm.typeOfEmployments}
              compare={(a) => a.name}
              render={(a) => a.name}
            /> */}
            <StagesForm vm={vm} />
          </div>
        </ChartSection>
        <div className="w-full flex justify-end">
          <Button onClick={() => vm.create()}>Создать вакансию</Button>
        </div>
      </div>
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/vacancy/new")({
  component: Page,
  beforeLoad: checkAuth,
  loader: async () => {
    return {};
  },
});
