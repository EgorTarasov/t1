from src import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
import sqlalchemy as sa


class Vacancy(Base):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    source: Mapped[str] = mapped_column(sa.Text, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    city: Mapped[str] = mapped_column(sa.Text, nullable=False)
    specialization: Mapped[str] = mapped_column(sa.Text, nullable=False)
    area: Mapped[str] = mapped_column(sa.Text, nullable=False)
    experience_from: Mapped[int] = mapped_column(sa.Integer)
    experience_to: Mapped[int] = mapped_column(sa.Integer)
    type_of_employment: Mapped[str] = mapped_column(sa.Text, nullable=False)

    def __repr__(self):
        return f"<Vacancy {self.id}>"
