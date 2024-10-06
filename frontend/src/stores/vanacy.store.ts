import { CandidatesEndpoint } from "@/api/endpoints/candidates.endpoint";
import { CandidatesDto } from "@/api/models/candidates.model";
import { mockVacancy, VacancyDto } from "@/api/models/vacancy.model";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable, observable } from "mobx";

export class VacancyStore implements DisposableVm {
  activeCandidates: CandidatesDto.ActiveCandidate[] = [];
  potentialCandidates: CandidatesDto.PotentialCandidate[] = [];
  declinedCandidates: CandidatesDto.DeclinedCandidate[] = [];

  constructor(public readonly vacancy: VacancyDto.DetailedItem) {
    makeAutoObservable(this);
  }

  async loadCandidates() {
    if (this.activeCandidates.length) return;

    const [active, potential, declined] = await Promise.all([
      CandidatesEndpoint.getActiveCandidates(this.vacancy.vacancy.id),
      CandidatesEndpoint.getPotentialCandidates(this.vacancy.vacancy.id),
      CandidatesEndpoint.getDeclinedCandidates(this.vacancy.vacancy.id),
    ]);

    this.activeCandidates = active.candidates;
    this.potentialCandidates = potential.candidates;
    this.declinedCandidates = declined.candidates;
  }

  dispose(): void {
    return;
  }
}
