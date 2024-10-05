import typing as tp
import datetime as dt
from pydantic import BaseModel, ConfigDict, Field
from src.hr.vacancy.schemas import VacancyDTO

if tp.TYPE_CHECKING:
    from src.hr.vacancy.schemas import VacancyDTO


class SkillBase(BaseModel):
    """SkillBase"""

    model_config = ConfigDict(from_attributes=True)

    name: str = Field("Python", title="Название навыка")


class SkillCreate(SkillBase):
    """Добавление навыка в общий пул"""


class SkillSearchResult(SkillBase):
    """Результат поиска навыка"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(1, title="ID навыка")


class CandidateDto(BaseModel):
    id: int = Field(..., description="")
    dob: dt.date = Field(..., description="")
    # Объединенение по ;
    spezialization: str = Field(..., description="")
    # Объединенение по ;
    education: str = Field(..., description="")
    candidate_skills: list[SkillSearchResult] = Field(
        None, description="List of skill IDs associated with candidate"
    )
    description: str = Field(..., description="")
    # Объединенение по :
    experience: str = Field(..., description="")
    cv_url: str = Field(..., description="")
    raw_json: dict[str, tp.Any] = Field(..., description="")
    src: str = Field(..., description="")
    vacancy: VacancyDTO | None = Field(None, description="")


class CandidateVacancyDto(BaseModel):
    candidate_id: int = Field(..., description="Id of candidate")
    date_of_accept: dt.datetime = Field(..., description="The education level required")
    stage_name: str = Field(..., description="")
    source: str = Field(..., description="")
    similarity: int = Field(..., description="")


class CandidateDeclineDto(BaseModel):
    candidate_id: int = Field(..., description="")
    date_of_decline: dt.datetime = Field(..., description="")
    reason: str = Field(..., description="")
    source: str = Field(..., description="")
    similarity: int = Field(..., description="")


class CandidatePotentialDto(BaseModel):
    source: str = Field(..., description="")
    similarity: int = Field(..., description="")


class AllCandidatesVacancyDto(BaseModel):
    vacancy: VacancyDTO = Field(..., description="Информация о вакансии")
    candidates: list[CandidateVacancyDto] = Field(..., description="")


class AllCandidatesDeclinedDto(BaseModel):
    vacancy: VacancyDTO = Field(..., description="Информация о вакансии")
    candidates: list[CandidateDeclineDto] = Field(..., description="")


class AllCandidatesPotentialDto(BaseModel):
    vacancy: VacancyDTO = Field(..., description="Информация о вакансии")
    candidates: list[CandidatePotentialDto] = Field(..., description="")


EXAMPLE_ALL_ACTIVE = [
    CandidateVacancyDto(
        candidate_id=1,
        date_of_accept=dt.datetime(2023, 10, 1, 14, 30),
        stage_name="Interview",
        source="LinkedIn",
        similarity=85,
    ),
    CandidateVacancyDto(
        candidate_id=2,
        date_of_accept=dt.datetime(2023, 10, 2, 9, 0),
        stage_name="Application Review",
        source="Employee Referral",
        similarity=90,
    ),
    CandidateVacancyDto(
        candidate_id=3,
        date_of_accept=dt.datetime(2023, 10, 3, 11, 15),
        stage_name="Offer Extended",
        source="Company Website",
        similarity=75,
    ),
    CandidateVacancyDto(
        candidate_id=4,
        date_of_accept=dt.datetime(2023, 10, 4, 16, 45),
        stage_name="Final Interview",
        source="Recruitment Agency",
        similarity=80,
    ),
    CandidateVacancyDto(
        candidate_id=5,
        date_of_accept=dt.datetime(2023, 10, 5, 10, 30),
        stage_name="Onboarding",
        source="Job Fair",
        similarity=88,
    ),
]

EXAMPLES_ALL_DECLINED = [
    CandidateDeclineDto(
        candidate_id=1,
        date_of_decline=dt.datetime(2023, 10, 1, 14, 30),
        reason="Accepted another offer",
        source="LinkedIn",
        similarity=85,
    ),
    CandidateDeclineDto(
        candidate_id=2,
        date_of_decline=dt.datetime(2023, 10, 2, 9, 0),
        reason="Salary expectations not met",
        source="Employee Referral",
        similarity=90,
    ),
    CandidateDeclineDto(
        candidate_id=3,
        date_of_decline=dt.datetime(2023, 10, 3, 11, 15),
        reason="Relocation issues",
        source="Company Website",
        similarity=75,
    ),
    CandidateDeclineDto(
        candidate_id=4,
        date_of_decline=dt.datetime(2023, 10, 4, 16, 45),
        reason="Personal reasons",
        source="Recruitment Agency",
        similarity=80,
    ),
    CandidateDeclineDto(
        candidate_id=5,
        date_of_decline=dt.datetime(2023, 10, 5, 10, 30),
        reason="Job role not aligned with career goals",
        source="Job Fair",
        similarity=88,
    ),
]

EXAMPLES_ALL_POTENTIAL = [
    CandidatePotentialDto(source="LinkedIn", similarity=92),
    CandidatePotentialDto(source="Employee Referral", similarity=85),
    CandidatePotentialDto(source="Company Website", similarity=78),
    CandidatePotentialDto(source="Recruitment Agency", similarity=88),
    CandidatePotentialDto(source="Job Fair", similarity=80),
]
