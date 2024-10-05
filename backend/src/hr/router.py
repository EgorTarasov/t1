from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger
from src.dependencies import get_db
import sqlalchemy as sa
import sqlalchemy.orm as orm
from .models import Vacancy, Skill, VacancySkill
from .schemas import VacancyCreate, SkillSearchResult, SkillCreate, VacancyDTO
from typing import Union

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(
    prefix="/vacancies",
    tags=["vacancies"],
)


# @router.get("/all/active", response_model=Page[VacancyDTO])
# async def return_active(
#     isAppointed: Union[bool, None] = None,
#     byDateDeadline: Union[bool, None] = None,
#     byDateCreation: Union[bool, None] = None,
#     byPriority: Union[str, None] = None,
#     db: AsyncSession = Depends(get_db),
# ):
#     stmt = (
#         sa.select(Vacancy)
#         .filter(
#             False
#             if isAppointed is None
#             else (
#                 Vacancy.recruiter_id != "0"
#                 if isAppointed
#                 else Vacancy.recruiter_id == "0"
#             )
#         )
#         .order_by(
#             False
#             if byPriority is None
#             else (Vacancy.priority if byPriority else Vacancy.priority.desc())
#         )
#         .order_by(
#             False
#             if byPriority is None
#             else (Vacancy.created_at if byDateCreation else Vacancy.created_at.desc())
#         )
#         .order_by(
#             False
#             if byPriority is None
#             else (Vacancy.deadline if byDateDeadline else Vacancy.deadline.desc())
#         )
#     )
#     return await paginate(db, stmt)
#     """
#     Returns all active vacancies in the database.

#     Args:
#         db (Session): The database session dependency.

#     Returns:
#         JSON: json containing all vacancies
#     """

#     return {"message": "Vacancies"}


@router.post("/new")
async def create_vacancy(
    vacancy: VacancyCreate,
    db: AsyncSession = Depends(get_db),
) -> int:
    # parse all skills and create them if they don't exist

    db_vacancy = Vacancy(
        name=vacancy.name,
        priority=vacancy.priority,
        deadline=vacancy.deadline,
        profession=vacancy.profession,
        area=vacancy.area,
        supervisor=vacancy.supervisor,
        city=vacancy.city,
        experience_from=vacancy.experience_from,
        experience_to=vacancy.experience_to,
        education=vacancy.education,
        quantity=vacancy.quantity,
        description=vacancy.description,
        type_of_employment=vacancy.type_of_employment,
    )
    stmt = sa.select(Skill).where(Skill.id.in_(vacancy.key_skills))

    required_skills = (await db.execute(stmt)).scalars()

    stmt = sa.select(Skill).where(Skill.id.in_(vacancy.additional_skills))

    additional_skills = (await db.execute(stmt)).scalars()

    db_vacancy.vacancy_skills = list(required_skills) + list(additional_skills)

    try:
        db.add(db_vacancy)
        await db.commit()
        await db.refresh(db_vacancy, attribute_names=["vacancy_skills"])
    except Exception as e:
        logger.error(f"Error: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")

    return db_vacancy.id


@router.get("/{vacancy_id}")
async def get_vacancy(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
) -> VacancyDTO:
    """Get vacancy by ID"""
    stmt = (
        sa.select(Vacancy)
        .options(
            orm.joinedload(
                Vacancy.vacancy_skills,
            ).joinedload(VacancySkill.skill)
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    skills = [vacancy_skill.skill for vacancy_skill in result.vacancy_skills]
    print(skills)
    return VacancyDTO.model_validate(result)


skills = APIRouter(
    prefix="/skills",
    tags=["skills"],
)


@skills.post("/new")
async def add_skill(
    skill: SkillCreate,
    db: AsyncSession = Depends(get_db),
) -> SkillSearchResult:
    """Добавление нового навыка"""
    db_skill = Skill(name=skill.name)
    db.add(db_skill)
    await db.commit()

    return SkillSearchResult(id=db_skill.id, name=db_skill.name)


@skills.get("/all")
async def get_skills(
    query: str = Query(
        None, title="запрос для поиска навыков", description="название навыка"
    ),
    db: AsyncSession = Depends(get_db),
) -> list[SkillSearchResult]:
    """Получение списка навыков для добавление не странице вакансии"""
    stmt = sa.select(Skill.id, Skill.name)

    if query:
        stmt = (
            sa.select(Skill.id, Skill.name)
            .where(Skill.name.ilike(f"%{query}%"))
            .limit(5)
        )
    else:
        stmt = stmt.limit(5)

    db_skills = await db.execute(stmt)
    results = db_skills.all()

    return [SkillSearchResult(id=skill.id, name=skill.name) for skill in results]


router.include_router(skills)
