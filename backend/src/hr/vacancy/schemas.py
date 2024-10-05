import typing as tp
import datetime as dt
from pydantic import BaseModel, ConfigDict, Field
from src.auth.schemas import UserDto
from src.hr.candidate.schemas import CandidateDto, SkillSearchResult

if tp.TYPE_CHECKING:
    from src.hr.candidate.schemas import CandidateDto


class VacancyCreate(BaseModel):
    """VacancyCreate

    Data required for vacancy creation

    Args:
        BaseModel (_type_): _description_
    """

    name: str = Field("Разработчик", title="Название вакансии")
    priority: int = Field(1, title="Приоритет")
    deadline: dt.datetime = Field(dt.datetime(2025, 1, 1), title="Срок подачи заявки")

    profession: str = Field("Программист", title="Профессия")
    area: str = Field("Разработка", title="Область занятости")
    supervisor: str = Field("Иванов Иван Иванович", title="Руководитель")

    city: str = Field("Москва", title="Город")

    # опыт работы, от до (лет)

    experience_from: int = Field(3, title="Опыт от")
    experience_to: int = Field(6, title="Опыт до")

    # образование
    education: str = Field("Высшее", title="Образование")

    # ключевые навыки
    key_skills: list[int] = Field([1, 2], title="Ключевые навыки")

    # количество открытых вакансий
    quantity: int = Field(1, title="Количество вакансий")

    # направление в компании
    direction: str = Field("Аналитика", title="Направление")

    # дополнительные навыки
    additional_skills: list[int] = Field([3], title="Дополнительные навыки")

    description: str = Field("Разработчик", title="Описание вакансии")

    type_of_employment: str = Field("Полная занятость", title="Тип занятости")


class VacancyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(None, description="The unique identifier of the vacancy")
    name: str = Field(..., description="The name of the vacancy")
    priority: int = Field(..., description="The priority of the vacancy")
    deadline: dt.datetime = Field(..., description="The deadline for the vacancy")
    profession: str = Field(..., description="The profession related to the vacancy")
    area: str = Field(..., description="The area of the vacancy")
    supervisor: str = Field(..., description="The supervisor of the vacancy")
    city: str = Field(..., description="The city where the vacancy is located")
    experience_from: tp.Optional[int] = Field(
        None, description="The minimum experience required"
    )
    experience_to: tp.Optional[int] = Field(
        None, description="The maximum experience required"
    )
    education: str = Field(..., description="The education level required")
    quantity: int = Field(..., description="The number of vacancies available")
    description: str = Field(..., description="The description of the vacancy")
    type_of_employment: str = Field(..., description="The type of employment")
    vacancy_skills: list[SkillSearchResult] = Field(
        None, description="List of skill IDs associated with the vacancy"
    )
    vacancy_candidates: list[CandidateDto] = Field(
        None, description="List of candidates IDs associated with vacancy"
    )

    recruiter: UserDto | None = Field(
        None, description="The recruiter assigned to the vacancy"
    )
    hr: UserDto | None = Field(None, description="The HR assigned to the vacancy")

    created_at: dt.datetime = Field(
        dt.datetime(2021, 1, 1),
        description="The creation date of the vacancy",
    )


class SourceDto(BaseModel):
    name: str = Field(..., description="Название источника")
    count: int = Field(..., description="Количество кандидатов с этого источника")
    percentage: float = Field(..., description="Процент кандидатов с этого источника")


class DeclineDto(BaseModel):
    reason: str = Field(..., description="Причина отказа")
    count: int = Field(..., description="Количество кандидатов с этой причиной")
    percentage: float = Field(..., description="Процент кандидатов с этой причиной")


class StageDto(BaseModel):
    id: int = Field(None, description="Уникальный идентификатор этапа")
    name: str = Field(..., description="Названия этапа для интерфейса")
    order: int = Field(..., description="Порядок этапа для отображения  воронки")
    success_rate: float = Field(
        ..., description="Процент прохождения на следующий этап"
    )
    avg_duration: int = Field(..., description="Средняя длительность этапа в днях")
    max_duration: int = Field(..., description="Максимальная длительность этапа в днях")
    number_of_candidates: int = Field(..., description="Количество кандидатов на этапе")
    sources: list[SourceDto] = Field(..., description="Информация об источниках")

    decline_reasons: list[DeclineDto] = Field(
        None, description="Причина отказа на этапе для всех кандидатов"
    )


class RoadmapDto(BaseModel):
    vacancy: VacancyDTO = Field(..., description="Информация о вакансии")
    stages: list[StageDto] = Field(..., description="Список этапов воронки")


EXAMPLE_STAGES = [
    StageDto(
        id=1,
        name="Hr скриннинг",
        order=1,
        success_rate=0.7,
        avg_duration=2,
        max_duration=20,
        number_of_candidates=100,
        sources=[
            SourceDto(name="hh.ru", count=50, percentage=50),
            SourceDto(name="linkedin", count=50, percentage=50),
        ],
        decline_reasons=[
            DeclineDto(reason="Не подходит", count=50, percentage=50),
            DeclineDto(reason="Не отвечает", count=50, percentage=50),
        ],
    ),
    StageDto(
        id=2,
        name="Телефонное интервью",
        order=2,
        success_rate=0.5,
        avg_duration=3,
        max_duration=15,
        number_of_candidates=50,
        sources=[
            SourceDto(name="hh.ru", count=25, percentage=50),
            SourceDto(name="linkedin", count=25, percentage=50),
        ],
        decline_reasons=[
            DeclineDto(reason="Не подходит", count=25, percentage=50),
            DeclineDto(reason="Не отвечает", count=25, percentage=50),
        ],
    ),
    StageDto(
        id=3,
        name="Финальное интервью",
        order=3,
        success_rate=0.3,
        avg_duration=5,
        max_duration=10,
        number_of_candidates=20,
        sources=[
            SourceDto(name="hh.ru", count=10, percentage=50),
            SourceDto(name="linkedin", count=10, percentage=50),
        ],
        decline_reasons=[
            DeclineDto(reason="Не подходит", count=10, percentage=50),
            DeclineDto(reason="Не отвечает", count=10, percentage=50),
        ],
    ),
    StageDto(
        id=4,
        name="Получение оффера",
        order=4,
        success_rate=0.9,
        avg_duration=1,
        max_duration=5,
        number_of_candidates=5,
        sources=[
            SourceDto(name="hh.ru", count=3, percentage=60),
            SourceDto(name="linkedin", count=2, percentage=40),
        ],
        decline_reasons=[
            DeclineDto(reason="Не подходит", count=3, percentage=60),
            DeclineDto(reason="Не отвечает", count=2, percentage=40),
        ],
    ),
    StageDto(
        id=5,
        name="выходит в штат",
        order=5,
        success_rate=1.0,
        avg_duration=0,
        max_duration=0,
        number_of_candidates=5,
        sources=[
            SourceDto(name="hh.ru", count=3, percentage=60),
            SourceDto(name="linkedin", count=2, percentage=40),
        ],
        decline_reasons=[
            DeclineDto(reason="Не подходит", count=0, percentage=0),
            DeclineDto(reason="Не отвечает", count=0, percentage=0),
        ],
    ),
]
