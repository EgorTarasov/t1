import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { ChartSection } from "@/components/pages/vacancy/chart-section";
import { IconInput } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Priority } from "@/types/priority.type";
import { checkAuth } from "@/utils/check-grant";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
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
import { StagesForm } from "@/components/pages/vacancy/StagesForm";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { DatePicker } from "@/components/ui/date-picker";

const Page = observer(() => {
  const vm = useViewModel(NewVacancyStore);
  const navigate = useNavigate();

  return (
    <MainLayout title="Новая вакансия">
      <div className="space-y-4">
        <ChartSection
          title="Основная информация"
          collapsible={false}
          allowOverflow
        >
          <div className="flex flex-col sm:flex-row sm:flex-wrap gap-4">
            <IconInput
              id="title"
              className="w-full sm:w-[300px]"
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
                <SelectTrigger id="priority" className="sm:w-[180px]">
                  <SelectValue placeholder="Выберите приоритет" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">{Priority.locale[1]}</SelectItem>
                  <SelectItem value="2">{Priority.locale[2]}</SelectItem>
                  <SelectItem value="3">{Priority.locale[3]}</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <IconInput
              label="Рекрутер"
              placeholder="Иванов Иван"
              // value={vm.supervisor}
              // onChange={(e) => {
              //   vm.supervisor = e.target.value;
              // }}
            />
            <div>
              <Label htmlFor="deadline">Дедлайн</Label>
              <DatePicker
                fromDate={new Date()}
                date={vm.deadline}
                setDate={(v) => v && (vm.deadline = v)}
              />
            </div>
            <IconInput
              label="Профессия"
              placeholder="Фронтенд разработчик"
              value={vm.profession}
              onChange={(e) => {
                vm.profession = e.target.value;
              }}
            />
            <IconInput
              label="Подразделение"
              placeholder="Отдел разработки"
              value={vm.area}
              onChange={(e) => {
                vm.area = e.target.value;
              }}
            />
            <IconInput
              label="Локация"
              placeholder="Москва"
              value={vm.city}
              onChange={(e) => {
                vm.city = e.target.value;
              }}
            />
            <IconInput
              label="Руководитель"
              placeholder="Иванов Иван"
              value={vm.supervisor}
              onChange={(e) => {
                vm.supervisor = e.target.value;
              }}
            />
          </div>
        </ChartSection>
        <ChartSection
          title="Основная информация"
          collapsible={false}
          allowOverflow
        >
          <div className="flex flex-col sm:flex-row sm:flex-wrap gap-4">
            <div className="grid grid-cols-[1fr_auto_1fr] w-fit items-center gap-x-1 h-fit">
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
                className="w-full sm:w-24"
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
                className="w-full sm:w-24"
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
          <div className="flex flex-col sm:grid grid-cols-2 w-full gap-6 gap-x-4">
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
            <div className="flex flex-col sm:grid grid-cols-2">
              <div className="grid grid-cols-[1fr_auto_1fr] w-full sm:w-fit items-center gap-x-1 h-fit">
                <Label
                  htmlFor="experience_from"
                  className="col-span-3 mt-1.5 mb-1"
                >
                  Вилка зарплаты, руб
                </Label>
                <IconInput
                  id="salary_low"
                  type="number"
                  placeholder="от"
                  onChange={(e) => {
                    vm.salaryLow = e.target.value;
                  }}
                  className="w-full sm:w-24"
                />
                <span>–</span>
                <IconInput
                  id="salary_high"
                  type="number"
                  placeholder="до"
                  value={vm.salaryHigh}
                  onChange={(e) => {
                    vm.salaryHigh = e.target.value;
                  }}
                  className="w-full sm:w-24"
                />
              </div>
            </div>
            <StagesForm vm={vm} />
          </div>
        </ChartSection>
        <div className="w-full flex sm:justify-end">
          <Button
            className="w-full sm:w-auto"
            onClick={() => {
              if (vm.validate()) {
                toast.promise(vm.create(navigate), {
                  loading: "Создание вакансии...",
                  success: "Вакансия создана",
                  error: "Ошибка создания вакансии",
                });
              }
            }}
          >
            Создать вакансию
          </Button>
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
