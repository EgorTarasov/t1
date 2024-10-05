import datetime as dt
import typing as tp

from pydantic import BaseModel, ConfigDict, Field


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
