import datetime as dt
from enum import unique

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
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
