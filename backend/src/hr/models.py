import datetime as dt
from enum import unique
import typing as tp
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import TimestampMixin
from src.database import Base


class Vacancy(Base, TimestampMixin):
    __tablename__ = "vacancies"
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
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    recruiter_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )
    hr_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )

    hr: Mapped["User"] = relationship("User", back_populates="my_vacancies")
    recruiter: Mapped["User"] = relationship(
        "User", back_populates="assigned_vacancies"
    )

    type_of_employment: Mapped[str] = mapped_column(sa.Text, nullable=False)
    vacancy_skills: Mapped[list["VacancySkill"]] = relationship(
        "VacancySkill", back_populates="vacancy"
    )

    def __repr__(self):
        return f"<Vacancy {self.id}>"


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False, unique=True)

    def __repr__(self):
        return f"<Skill {self.name}>"


class VacancySkill(Base):
    __tablename__ = "vacancy_skills"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("vacancies.id"), nullable=False
    )
    skill_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("skills.id"), nullable=False
    )
    is_key_skill: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(
        "Vacancy", back_populates="vacancy_skills"
    )
    skill: Mapped["Skill"] = relationship("Skill")

    def __repr__(self):
        return f"<VacancySkill vacancy_id={self.vacancy_id} skill_id={self.skill_id} is_key_skill={self.is_key_skill}>"


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("candidates.id"), nullable=False
    )
    skill_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("skills.id"), nullable=False
    )
    vacancy: Mapped["Vacancy"] = relationship(
        "Candidate", back_populates="candidate_skills"
    )
    skill: Mapped["Skill"] = relationship("Skill")

    def __repr__(self):
        return (
            f"<CandidateSkill canidate_id={self.vacancy_id} skill_id={self.skill_id}>"
        )


class Roadmap(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("vacancies.id"), nullable=False
    )
    vacancy = relationship("Vacancy")

    def __repr__(self):
        return f"<Roadmap {self.id} >"


class RoadmapStage(Base, TimestampMixin):
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
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    dob: Mapped[dt.date] = mapped_column(sa.Date, nullable=False)
    # Объединенение по ;
    spezialization: Mapped[str] = mapped_column(sa.Text, nullable=False)
    # Объединенение по ;
    education: Mapped[str] = mapped_column(sa.Text, nullable=False)
    candidate_skills: Mapped[list["CandidateSkill"]] = relationship(
        "CandidateSkill", back_populates="Candidate"
    )
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    # Объединенение по :
    experience: Mapped[str] = mapped_column(sa.Text, nullable=False)
    cv_url: Mapped[str] = mapped_column(sa.Text, nullable=False)
    raw_json: Mapped[dict[str, tp.Any]] = mapped_column(JSON, nullable=False)
    src: Mapped[str] = mapped_column(sa.Text, default="hh", nullable=False)


class RoadMapStageCompletion(Base):
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
