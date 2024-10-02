import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.dependencies import DatabaseMiddleware
from .schemas import VacancyCreate, VacancyDto
from .models import Vacancy
from src.serializers.vacancy import db_vacancy_to_vacancy_dto
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy import orm
import json

router = APIRouter(
    prefix="/vacancies",
)


@router.get("/refresh")
async def return_active(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    """
    Updates db of all active vacancies and returns all active vacancies in the database.

    Args:
        db (Session): The database session dependency.

    Returns:
        JSON: json containing all vacancies
    """

    return {"message": "Vacancies"}


@router.post("/new")
async def set_new(
    vacancy: VacancyCreate,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    """
    Returns all active vacancies in the database.

    Args:
        vacancy (VacancyCreate): Vacancy information to create.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating that vacancy has been registered.
    """

    db_vacancy = Vacancy(
        name=vacancy.name,
        source=str(vacancy.source),
        description=vacancy.description,
        city=vacancy.city,
        specialization=vacancy.specialization,
        area=vacancy.area,
        experience_from=vacancy.experience_from,
        experience_to=vacancy.experience_to,
        type_of_employment=vacancy.type_of_employment,
        key_skills=vacancy.key_skills,
    )
    try:
        db.add(db_vacancy)
        await db.flush()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Error while adding vacancy")
    await db.commit()
    return {"message": "Vacancy created"}


@router.get("/id/{vacancy_id}", response_model=VacancyDto)
async def get_by_id(
    vacancy_id: int,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    """
    Returns vacancy by id in the database.

    Args:
        vacancy_id (Integer): Vacancy id in database.
        db (Session): The database session dependency.

    Returns:
        JSON: vacancy information in json
    """

    stmt = sa.select(Vacancy).where(Vacancy.id == vacancy_id)
    db_vacancy = (await db.execute(stmt)).scalar()
    return db_vacancy_to_vacancy_dto(db_vacancy)
