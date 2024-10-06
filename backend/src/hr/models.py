import datetime as dt
from enum import unique
import typing as tp
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.database import Base
from src.models import TimestampMixin

if tp.TYPE_CHECKING:
    from src.auth.models import User


class Vacancy(Base, TimestampMixin):
    __tablename__ = "vacancies"  # type: ignore

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    priority: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    deadline: Mapped[dt.datetime] = mapped_column(sa.DateTime, nullable=False)
    profession: Mapped[str] = mapped_column(sa.Text, nullable=False)
    area: Mapped[str] = mapped_column(sa.Text, nullable=False)
    supervisor: Mapped[str] = mapped_column(sa.Text, nullable=False)
    city: Mapped[str] = mapped_column(sa.Text, nullable=False)
    experience_from: Mapped[int] = mapped_column(sa.Integer)
    experience_to: Mapped[int] = mapped_column(sa.Integer)
    education: Mapped[str] = mapped_column(sa.Text, nullable=False)
    quantity: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    direction: Mapped[str] = mapped_column(sa.Text, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    recruiter_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )
    salary_high: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=30_000,
        server_default="30000",
    )
    salary_low: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=70_000,
        server_default="70000",
    )
    hr_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )

    hr = relationship(
        "User",
        back_populates="my_vacancies",
        primaryjoin="User.id == Vacancy.hr_id",
    )
    recruiter = relationship(
        "User",
        back_populates="assigned_vacancies",
        primaryjoin="User.id == Vacancy.recruiter_id",
    )

    # candidates_ids: Mapped[list[int]] = mapped_column()

    vacancy_candidates = relationship(
        "Candidate",
        back_populates="vacancies",
        secondary="vacancy_candidates",
    )
    type_of_employment: Mapped[str] = mapped_column(sa.Text, nullable=False)
    vacancy_skills = relationship(
        "Skill",
        back_populates="vacancies",
        secondary="vacancy_skills",
    )
    # required_skills: Mapped[str] = mapped_column(sa.Text, nullable=False)

    def __repr__(self):
        return f"<Vacancy {self.id}>"


class VacancySkill(Base):
    __tablename__ = "vacancy_skills"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("vacancies.id"), nullable=False
    )
    skill_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("skills.id"), nullable=False
    )
    is_key_skill: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)

    def __repr__(self):
        return f"<VacancySkill vacancy_id={self.vacancy_id} skill_id={self.skill_id} is_key_skill={self.is_key_skill}>"


class VacancyCandidates(Base):
    __tablename__ = "vacancy_candidates"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("vacancies.id"), nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("candidates.id"), nullable=False
    )

    def __repr__(self):
        return f"<VacancySkill vacancy_id={self.vacancy_id}>"


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("candidates.id"), nullable=False
    )
    skill_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("skills.id"), nullable=False
    )

    def __repr__(self):
        return (
            f"<CandidateSkill canidate_id={self.candidate_id} skill_id={self.skill_id}>"
        )


class Roadmap(Base, TimestampMixin):
    """Воронка"""

    __tablename__ = "roadmaps"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("vacancies.id"), nullable=False
    )
    vacancy = relationship("Vacancy")

    def __repr__(self):
        return f"<Roadmap {self.id} >"


class RoadmapStage(Base, TimestampMixin):
    """Этапы воронки"""

    __tablename__ = "roadmap_stages"  # type: ignore

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    roadmap_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("roadmaps.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    order: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    # продолжительность в днях
    duration: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    roadmap = relationship("Roadmap")


class Candidate(Base):
    """Кандидаты"""


    __tablename__ = "candidates"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    dob: Mapped[dt.date] = mapped_column(sa.Date, nullable=False)
    # Объединенение по ;
    spezialization: Mapped[str] = mapped_column(sa.Text, nullable=False)
    # Объединенение по ;
    education: Mapped[list[dict[str, tp.Any]]] = mapped_column(JSON, nullable=False)
    candidate_skills = relationship(
        "Skill",
        back_populates="candidates",
        secondary="candidate_skills",
    )
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    # Объединенение по :
    experience: Mapped[list[dict[str, tp.Any]]] = mapped_column(JSON, nullable=False)
    cv_url: Mapped[str] = mapped_column(sa.Text, nullable=False)
    raw_json: Mapped[dict[str, tp.Any]] = mapped_column(JSON, nullable=False)
    src: Mapped[str] = mapped_column(sa.Text, default="hh", nullable=False)

    vacancies = relationship(
        "Vacancy",
        back_populates="vacancy_candidates",
        secondary="vacancy_candidates",
    )


class RoadMapStageCompletion(Base):
    """Завершение этапа воронки"""

    __tablename__ = "roadmap_stage_completions"  # type: ignore

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("candidates.id")
    )
    stage_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("roadmap_stages.id")
    )
    completed_at: Mapped[dt.datetime] = mapped_column(sa.DateTime, default=None)
    created_at: Mapped[dt.datetime] = mapped_column(sa.DateTime, default=None)
    declined: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    reason_of_decline: Mapped[str | None] = mapped_column(sa.Text, default=None)


class Skill(Base):
    __tablename__ = "skills"  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False, unique=True)
    vacancies = relationship(
        "Vacancy",
        back_populates="vacancy_skills",
        secondary="vacancy_skills",
    )
    candidates = relationship(
        "Candidate",
        back_populates="candidate_skills",
        secondary="candidate_skills",
    )

    def __repr__(self):
        return f"<Skill {self.name}>"
