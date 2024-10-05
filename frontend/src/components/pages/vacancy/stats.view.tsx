import { VacancyDto } from "@/api/models/vacancy.model";
import { observer } from "mobx-react-lite";
import { FC, useState, useMemo } from "react";
import { ChartSection } from "./chart-section";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/utils/cn";
import DropdownMultiple from "@/components/DropdownMultiple";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface Props {
  vacancy: VacancyDto.DetailedItem;
}

const COLORS = [
  "bg-teal-300",
  "bg-indigo-300",
  "bg-blue-300",
  "bg-yellow-300",
  "bg-orange-300",
  "bg-green-300",
  "bg-red-300",
  "bg-purple-300",
  "bg-pink-300",
  "bg-gray-300",
];

export const Stats: FC<Props> = observer((x) => {
  const firstStageCount = useMemo(() => {
    return x.vacancy.stages[0].sources.reduce((acc, curr) => {
      return acc + curr.count;
    }, 0);
  }, [x.vacancy.stages]);

  const assignedColors = useMemo(() => {
    const colors: Record<string, string> = {};
    x.vacancy.stages[0].sources.forEach((v, i) => {
      colors[v.name] = COLORS[i % COLORS.length];
    });
    return colors;
  }, [x.vacancy.stages]);

  const sourcesCount: Record<string, number> = useMemo(() => {
    return x.vacancy.stages[0].sources.reduce((acc, curr) => {
      const name = curr.name;
      const count = x.vacancy.stages.reduce((acc, curr) => {
        return acc + (curr.sources.find((v) => v.name === name)?.count || 0);
      }, 0);
      return { ...acc, [name]: count };
    }, {});
  }, [x.vacancy.stages]);

  const assignedDeclineColors: Record<string, string> = useMemo(() => {
    const colors: Record<string, string> = {};
    x.vacancy.stages[0].decline_reasons.forEach((v, i) => {
      colors[v.reason] = COLORS[i % COLORS.length];
    });
    return colors;
  }, [x.vacancy.stages]);

  const declineReasonsCount: Record<string, number> = useMemo(() => {
    return x.vacancy.stages[0].decline_reasons.reduce((acc, curr) => {
      const name = curr.reason;
      const count = x.vacancy.stages.reduce((acc, curr) => {
        return (
          acc +
          (curr.decline_reasons.find((v) => v.reason === name)?.count || 0)
        );
      }, 0);
      return { ...acc, [name]: count };
    }, {});
  }, [x.vacancy.stages]);

  return (
    <div className="space-y-5">
      <ChartSection
        title="Воронка найма по вакансии"
        description="На этапе “Получение оффера” отваливается слишком много людей. Убедитесь, что вакансия соответствует зарплатным ожиданиям кандидата."
      >
        <div className="space-y-1">
          <h3 className="text-lg font-medium text-slate-700">Этапы</h3>
          <ul className="grid grid-cols-[auto_1fr_100px_auto] gap-1 min-w-[250px]">
            {x.vacancy.stages.map((stage, i) => {
              return (
                <li key={i} className="contents *:rounded-lg *:h-8 text-sm">
                  <div className="flex items-center justify-center min-w-8 bg-slate-200">
                    {i + 1}
                  </div>
                  <div className="flex items-center px-3 bg-primary overflow-hidden">
                    <p className="truncate text-white">{stage.name}</p>
                  </div>
                  <div className="relative">
                    <Progress
                      value={stage.success_rate * 100}
                      className="bg-slate-200 h-8 rounded-lg"
                      indicatorClassName={cn(
                        "rounded-lg",
                        stage.success_rate > 0.5
                          ? "bg-green-200"
                          : "bg-red-200",
                      )}
                    />
                    <p className="absolute inset-0 flex items-center justify-center">
                      {stage.success_rate * 100}%
                    </p>
                  </div>
                  <div className="flex items-center h-8 px-2">
                    {stage.number_of_candidates}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
        <div className="space-y-1">
          <h3 className="text-lg font-medium text-slate-700 text-nowrap">
            Среднее время прохождения
          </h3>
          <ul className="grid grid-cols-[auto_100px] gap-1 w-fit">
            {x.vacancy.stages.map((stage, i) => {
              const duration = (stage.avg_duration / stage.max_duration) * 100;

              return (
                <li key={i} className="contents *:rounded-lg *:h-8 text-sm">
                  <div className="flex items-center justify-center min-w-8 bg-slate-200">
                    {i + 1}
                  </div>
                  <div className="relative">
                    <Progress
                      value={duration}
                      className="bg-slate-200 h-8 rounded-lg"
                      indicatorClassName={cn(
                        "rounded-lg",
                        duration <= 100 ? "bg-green-200" : "bg-red-200",
                      )}
                    />
                    <p className="absolute inset-0 flex items-center justify-center">
                      {stage.avg_duration} / {stage.max_duration} дн.
                    </p>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      </ChartSection>
      <ChartSection
        title="Эффективность источников подбора"
        description="Вы используете не самые эффективные источники найма. Обращайте больше внимание на вакансии из источника “Реффер”"
      >
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-medium text-slate-700">По этапам</h3>
          <TooltipProvider delayDuration={0}>
            <ul className="flex flex-col gap-1">
              {x.vacancy.stages.map((stage, i) => {
                const stageCount = stage.sources.reduce((acc, curr) => {
                  return acc + curr.count;
                }, 0);

                const percentageFromFirstStage =
                  (stageCount / firstStageCount) * 100;

                return (
                  <li key={i} className="flex *:rounded-lg *:h-8 text-sm gap-1">
                    <div className="flex items-center justify-center min-w-8 bg-slate-200">
                      {i + 1}
                    </div>
                    <div
                      className="flex *:rounded-lg *:h-8 w-full space-x-1"
                      style={{ width: `${percentageFromFirstStage}%` }}
                    >
                      {stage.sources.map((source, i) => {
                        return (
                          <Tooltip key={i}>
                            <TooltipTrigger asChild>
                              <div
                                style={{
                                  width: `${(source.count / stageCount) * 100}%`,
                                }}
                                className={cn(
                                  "flex items-center justify-center",
                                  assignedColors[source.name],
                                )}
                              />
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>
                                {source.name} – {source.count}
                              </p>
                            </TooltipContent>
                          </Tooltip>
                        );
                      })}
                    </div>
                  </li>
                );
              })}
            </ul>
          </TooltipProvider>
        </div>
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-medium text-slate-700">По этапам</h3>
          <ul className="flex flex-wrap gap-1">
            {Object.entries(sourcesCount).map(([stage, count], i) => {
              return (
                <li
                  key={i}
                  className={cn(
                    "flex items-center rounded-lg h-8 px-2 text-sm gap-2",
                    assignedColors[stage],
                  )}
                >
                  <span>{stage}</span>
                  <span>{count}</span>
                </li>
              );
            })}
          </ul>
        </div>
      </ChartSection>
      <ChartSection
        title="Причины отсева"
        description="Вы просматриваете слишком много людей, которые не знают грузинский"
      >
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-medium text-slate-700">По этапам</h3>
          <TooltipProvider delayDuration={0}>
            <ul className="flex flex-col gap-1">
              {x.vacancy.stages.map((stage, i) => {
                const stageCount = stage.decline_reasons.reduce((acc, curr) => {
                  return acc + curr.count;
                }, 0);

                const percentageFromFirstStage =
                  (stageCount / firstStageCount) * 100;

                return (
                  <li key={i} className="flex *:rounded-lg *:h-8 text-sm gap-1">
                    <div className="flex items-center justify-center min-w-8 bg-slate-200">
                      {i + 1}
                    </div>
                    <div
                      className="flex *:rounded-lg *:h-8 w-full space-x-1"
                      style={{ width: `${percentageFromFirstStage}%` }}
                    >
                      {stage.decline_reasons.map((source, i) => {
                        return (
                          <Tooltip key={i}>
                            <TooltipTrigger asChild>
                              <div
                                style={{
                                  width: `${(source.count / stageCount) * 100}%`,
                                }}
                                className={cn(
                                  "flex items-center justify-center",
                                  assignedDeclineColors[source.reason],
                                )}
                              />
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>
                                {source.reason} – {source.count}
                              </p>
                            </TooltipContent>
                          </Tooltip>
                        );
                      })}
                    </div>
                  </li>
                );
              })}
            </ul>
          </TooltipProvider>
        </div>
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-medium text-slate-700">По этапам</h3>
          <ul className="flex flex-wrap gap-1">
            {Object.entries(declineReasonsCount).map(([stage, count], i) => {
              return (
                <li
                  key={i}
                  className={cn(
                    "flex items-center rounded-lg h-8 px-2 text-sm gap-2",
                    assignedDeclineColors[stage],
                  )}
                >
                  <span>{stage}</span>
                  <span>{count}</span>
                </li>
              );
            })}
          </ul>
        </div>
      </ChartSection>
    </div>
  );
});
