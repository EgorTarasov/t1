import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.dependencies import DatabaseMiddleware
from .schemas import VacancyCreate
from .models import Vacancy

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy import orm

router = APIRouter(
    prefix="/vacancies",
)


@router.get("/all/active")
async def return_active(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(DatabaseMiddleware.get_session),
):
    """
    Returns all active vacancies in the database.

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
    )
    try:
        db.add(db_vacancy)
        await db.flush()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Error while adding vacancy")
    await db.commit()
