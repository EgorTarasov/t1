from typing import List

from src.hr.models import Vacancy
from src.hr.schemas import VacancyDto


def db_vacancy_to_vacancy_dto(db_vacancy: Vacancy):
    return VacancyDto.model_validate(
        {
            "id": db_vacancy.id,
            "source": db_vacancy.source,
            "description": db_vacancy.description,
            "city": db_vacancy.city,
            "specialization": db_vacancy.specialization,
            "area": db_vacancy.area,
            "experience_from": db_vacancy.experience_from,
            "experience_to": db_vacancy.experience_to,
            "type_of_employment": db_vacancy.type_of_employment,
            "key_skills": db_vacancy.key_skills,
        }
    )
