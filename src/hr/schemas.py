from pydantic import BaseModel, Field, HttpUrl


class VacancyCreate(BaseModel):
    """VacancyCreate

    Data required for vacancy creation

    Args:
        BaseModel (_type_): _description_
    """

    name: str = Field("Разработчик", title="Название вакансии")
    source: HttpUrl = Field(".com", title="Ссылка на вакансию")
    description: str = Field("Разработчик", title="Описание вакансии")
    city: str = Field("Москва", title="Город")
    specialization: str = Field("Программист, разработчик", title="Специализация")
    area: str = Field("Разработка", title="Область занятости")
    experience_from: int = Field(3, title="Опыт от")
    experience_to: int = Field(6, title="Опыт до")
    type_of_employment: str = Field("Полная занятость", title="Тип занятости")
    key_skills: list = Field(["Python"], title="Ключевые навыки")


class VacancyDto(BaseModel):
    id: int
    source: str
    description: str
    city: str
    specialization: str
    area: str
    experience_from: int
    experience_to: int
    type_of_employment: str
    key_skills: list
