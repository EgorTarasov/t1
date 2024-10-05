from typing import List, Union

import sqlalchemy as sa
import sqlalchemy.orm as orm
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db

from .models import Skill, Vacancy
from .schemas import (EXAMPLE_ALL_ACTIVE, EXAMPLE_STAGES,
                      EXAMPLES_ALL_DECLINED, EXAMPLES_ALL_POTENTIAL,
                      AllCandidatesDeclinedDto, AllCandidatesPotentialDto,
                      AllCandidatesVacancyDto, CandidateDto, RoadmapDto,
                      SkillCreate, SkillSearchResult, VacancyCreate,
                      VacancyDTO)

router = APIRouter(
    prefix="/vacancies",
    tags=["vacancies"],
)


@router.get("/all/active", response_model=Page[VacancyDTO])
async def return_active(
    isAppointed: Union[bool, None] = None,
    byDateDeadline: Union[bool, None] = None,
    byDateCreation: Union[bool, None] = None,
    byPriority: Union[bool, None] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Args:
        db (Session): The database session dependency.
        isAppointed(bool): Is the vacancy appointed to recruiter/hr
        byDateDeadline(bool):
        byDateCreation(bool):
        byPriority(bool):
    Returns:
        JSON: json containing all vacancies
    """

    # TODO: check join statement
    stmt = sa.select(Vacancy).options(
        orm.joinedload(Vacancy.vacancy_skills),
        orm.joinedload(Vacancy.recruiter),
        orm.joinedload(Vacancy.hr),
    )
    if isAppointed is not None:
        stmt = stmt.filter(
            Vacancy.recruiter_id != None
            if isAppointed
            else Vacancy.recruiter_id == None
        )
    if byPriority is not None:
        stmt = stmt.order_by(
            Vacancy.priority if byPriority else Vacancy.priority.desc()
        )
    if byDateCreation is not None:
        stmt = stmt.order_by(
            Vacancy.created_at if byDateCreation else Vacancy.created_at.desc()
        )
    if byDateDeadline is not None:
        stmt = stmt.order_by(
            Vacancy.deadline if byDateDeadline else Vacancy.deadline.desc()
        )

    return await paginate(db, stmt)


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
        direction=vacancy.direction,
        description=vacancy.description,
        type_of_employment=vacancy.type_of_employment,
    )
    stmt = sa.select(Skill).where(Skill.id.in_(vacancy.key_skills))

    required_skills = (await db.execute(stmt)).scalars()

    stmt = sa.select(Skill).where(Skill.id.in_(vacancy.additional_skills))

    additional_skills = (await db.execute(stmt)).scalars()

    db_vacancy.vacancy_skills = list(required_skills) + list(additional_skills)  # type: ignore

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
            )
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return VacancyDTO.model_validate(result)


@router.get("/roadmap/{vacancy_id}")
async def get_vacancy_roadmap(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
) -> RoadmapDto:
    """Get vacancy roadmap by ID"""
    stmt = (
        sa.select(Vacancy)
        .options(
            orm.joinedload(
                Vacancy.vacancy_skills,
            )
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return RoadmapDto(vacancy=VacancyDTO.model_validate(result), stages=EXAMPLE_STAGES)


@router.get("/candidates/active/{vacancy_id}")
async def get_active_vacancies(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
) -> AllCandidatesVacancyDto:
    """Get vacancy roadmap by ID"""
    stmt = (
        sa.select(Vacancy)
        .options(
            orm.joinedload(
                Vacancy.vacancy_skills,
            ),
            orm.joinedload(
                Vacancy.vacancy_candidates,
            ),
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return AllCandidatesVacancyDto(
        vacancy=VacancyDTO.model_validate(result), candidates=EXAMPLE_ALL_ACTIVE
    )


@router.get("/candidates/declined/{vacancy_id}")
async def get_declined_vacancies(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
) -> AllCandidatesDeclinedDto:
    """Get vacancy roadmap by ID"""
    stmt = (
        sa.select(Vacancy)
        .options(
            orm.joinedload(
                Vacancy.vacancy_skills,
            ),
            orm.joinedload(
                Vacancy.vacancy_candidates,
            ),
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return AllCandidatesDeclinedDto(
        vacancy=VacancyDTO.model_validate(result), candidates=EXAMPLES_ALL_DECLINED
    )


@router.get("/candidates/potential/{vacancy_id}")
async def get_potential_vacancies(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
) -> AllCandidatesPotentialDto:
    """Get vacancy roadmap by ID"""
    stmt = (
        sa.select(Vacancy)
        .options(
            orm.joinedload(
                Vacancy.vacancy_skills,
            ),
            orm.joinedload(
                Vacancy.vacancy_candidates,
            ),
        )
        .filter(Vacancy.id == vacancy_id)
    )
    db_vacancy = await db.execute(stmt)
    result: Vacancy | None = db_vacancy.unique().scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return AllCandidatesPotentialDto(
        vacancy=VacancyDTO.model_validate(result), candidates=EXAMPLES_ALL_POTENTIAL
    )


skills = APIRouter(
    prefix="/skills",
    tags=["skills"],
)


@skills.post("/new")
async def add_skill(
    skills: List[SkillCreate],
    db: AsyncSession = Depends(get_db),
) -> list[SkillSearchResult]:
    """Добавление нового навыка"""
    db_skills = []
    for skill in skills:
        db_skill = Skill(name=skill.name)
        db.add(db_skill)
        await db.flush()
        await db.refresh(db_skill, ["id"])
        db_skills.append(db_skill)
    await db.commit()
    return [SkillSearchResult.model_validate(obj) for obj in db_skills]


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
