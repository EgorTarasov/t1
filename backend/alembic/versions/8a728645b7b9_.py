"""

Revision ID: 8a728645b7b9
Revises: 9a2e09095721
Create Date: 2024-10-05 21:30:25.112259

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a728645b7b9'
down_revision: Union[str, None] = '9a2e09095721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacancy_candidates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy_candidates')
    # ### end Alembic commands ###
