import { CandidatesEndpoint } from "@/api/endpoints/candidates.endpoint";
import { CandidatesDto } from "@/api/models/candidates.model";
import { mockVacancy, VacancyDto } from "@/api/models/vacancy.model";
import { DisposableVm } from "@/utils/vm";
import { makeAutoObservable, observable } from "mobx";

export class VacancyStore implements DisposableVm {
  candidatesLoaded = false;
  activeCandidates: CandidatesDto.ActiveCandidate[] = [];
  potentialCandidates: CandidatesDto.PotentialCandidate[] = [];
  declinedCandidates: CandidatesDto.DeclinedCandidate[] = [];

  analytics: CandidatesDto.Analytics | null = null;

  constructor(public readonly vacancy: VacancyDto.DetailedItem) {
    makeAutoObservable(this);
  }

  async loadCandidates() {
    if (this.candidatesLoaded) return;

    const [active, potential, declined] = await Promise.all([
      CandidatesEndpoint.getActiveCandidates(this.vacancy.vacancy.id),
      CandidatesEndpoint.getPotentialCandidates(this.vacancy.vacancy.id),
      CandidatesEndpoint.getDeclinedCandidates(this.vacancy.vacancy.id),
    ]);

    this.activeCandidates = active.candidates;
    this.potentialCandidates = potential.candidates;
    this.declinedCandidates = declined.candidates;

    this.candidatesLoaded = true;
  }

  async fetchAnalytics() {
    if (this.analytics) return;

    this.analytics = await CandidatesEndpoint.getAnalytics(
      this.vacancy.vacancy.id,
    );
  }

  dispose(): void {
    return;
  }
}
