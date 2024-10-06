import { VacancyEndpoint } from "@/api/endpoints/vacanvy.endpoint";
import { mockVacancy } from "@/api/models/vacancy.model";
import { MainLayout } from "@/components/hoc/layouts/main.layout";
import { AnalyticsView } from "@/components/pages/vacancy/analytics.view";
import { CandidatesView } from "@/components/pages/vacancy/candidates.view";
import { OverviewView } from "@/components/pages/vacancy/overview.view";
import { Stats } from "@/components/pages/vacancy/stats.view";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { VacancyStore } from "@/stores/vanacy.store";
import { Priority } from "@/types/priority.type";
import { checkAuth } from "@/utils/check-grant";
import { pluralize } from "@/utils/pluralize";
import { useViewModel } from "@/utils/vm";
import {
  createFileRoute,
  useLoaderData,
  useNavigate,
  useSearch,
} from "@tanstack/react-router";
import { observer } from "mobx-react-lite";
import { useState } from "react";
import { z } from "zod";

const Page = observer(() => {
  const { vacancy } = Route.useLoaderData();
  const [tab, setTab] = useState(
    new URLSearchParams(window.location.search).get("tab") ?? "overview",
  );
  const vm = useViewModel(VacancyStore, vacancy);

  const deadline = new Date(vm.vacancy.vacancy.deadline);
  const createdAt = new Date(vm.vacancy.vacancy.created_at);
  const dateNow = new Date();

  const totalDuration = deadline.getTime() - createdAt.getTime();
  const timePassed = dateNow.getTime() - createdAt.getTime();

  const daysLeft = Math.ceil(
    (deadline.getTime() - dateNow.getTime()) / (1000 * 60 * 60 * 24),
  );

  const percentage = Math.min((timePassed / totalDuration) * 100, 100);

  return (
    <MainLayout
      header={
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 pr-12 sm:pr-0">
            {vm.vacancy.vacancy.name}
          </h1>
          <p className="text-slate-500">{vm.vacancy.vacancy.area}</p>
          <div className="flex justify-between md:items-end gap-2 flex-col md:flex-row">
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="space-y-2 md:basis-[300px] w-full md:w-auto">
                  <span className="flex items-center text-slate-800">
                    {deadline.toLocaleDateString("ru-RU")}
                    {daysLeft > 0 && (
                      <>
                        <div className="rounded-full bg-slate-500 min-w-2 size-2 inline-block mx-2"></div>
                        ещё {daysLeft}{" "}
                        {pluralize(daysLeft, ["день", "дня", "дней"])}
                      </>
                    )}
                  </span>
                  <Progress value={percentage} className="basis-[300px] h-2" />
                </div>
              </TooltipTrigger>
              <TooltipContent>
                Начало: {createdAt.toLocaleDateString("ru-RU")}
                <br />
                Дедлайн: {deadline.toLocaleDateString("ru-RU")}
              </TooltipContent>
            </Tooltip>
            <div>
              <Label htmlFor="priority">Приоритет</Label>
              <Select
                key={vm.vacancy.vacancy.priority}
                value={vm.vacancy.vacancy.priority.toString()}
                onValueChange={(value) => {
                  vm.vacancy!.vacancy.priority = Number(value);
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
        </div>
      }
    >
      <Accordion type="single" collapsible className="sm:hidden">
        <AccordionItem value="overview">
          <AccordionTrigger>О вакансии</AccordionTrigger>
          <AccordionContent>
            <OverviewView vm={vm} />
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="stats">
          <AccordionTrigger>Статистика по вакансии</AccordionTrigger>
          <AccordionContent>
            <Stats vacancy={vm.vacancy} />
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="candidates">
          <AccordionTrigger>Кандидаты</AccordionTrigger>
          <AccordionContent>
            <CandidatesView vm={vm} />
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="analytics">
          <AccordionTrigger>Анализ рынка по вакансии</AccordionTrigger>
          <AccordionContent>
            <AnalyticsView vm={vm} />
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <div className="hidden sm:block">
        <Tabs value={tab} onValueChange={(value) => setTab(value)}>
          <TabsList className="overflow-x-auto">
            <TabsTrigger value="overview">О вакансии</TabsTrigger>
            <TabsTrigger value="stats">Статистика по вакансии</TabsTrigger>
            <TabsTrigger value="candidates">Кандидаты</TabsTrigger>
            <TabsTrigger value="analytics">
              Анализ рынка по вакансии
            </TabsTrigger>
          </TabsList>
          <TabsContent value="overview">
            <OverviewView vm={vm} />
          </TabsContent>
          <TabsContent value="stats">
            <Stats vacancy={vm.vacancy} />
          </TabsContent>
          <TabsContent value="candidates">
            <CandidatesView vm={vm} />
          </TabsContent>
          <TabsContent value="analytics">
            <AnalyticsView vm={vm} />
          </TabsContent>
        </Tabs>
      </div>
    </MainLayout>
  );
});

export const Route = createFileRoute("/_base/vacancy/$id")({
  component: Page,
  beforeLoad: checkAuth,
  loader: async (x) => {
    const vacancy = await VacancyEndpoint.getById(x.params.id);
    return { vacancy };
  },
});
