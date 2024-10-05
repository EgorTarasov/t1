"""Roadmap

Revision ID: dc870f149407
Revises: 96495df9ff1f
Create Date: 2024-10-05 12:36:04.607924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc870f149407'
down_revision: Union[str, None] = '96495df9ff1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('spezialization', sa.Text(), nullable=False),
    sa.Column('education', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('experience', sa.Text(), nullable=False),
    sa.Column('cv_url', sa.Text(), nullable=False),
    sa.Column('raw_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('src', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('candidate_skills',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('road_map_stage_completions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('stage_id', sa.Integer(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('declined', sa.Boolean(), nullable=False),
    sa.Column('reason_of_decline', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['stage_id'], ['roadmap_stages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('roadmap_stages', sa.Column('order', sa.Integer(), nullable=False))
    op.add_column('roadmap_stages', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('roadmap_stages', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.alter_column('roadmap_stages', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('roadmap_stages', 'roadmap_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('roadmap_stages', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('roadmap_stages', 'duration',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('roadmaps', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('roadmaps_id_seq'::regclass)"))
    op.alter_column('roadmaps', 'vacancy_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('roadmaps', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('roadmaps', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_column('roadmaps', 'deadline')
    op.drop_column('roadmaps', 'deleted_at')
    op.add_column('vacancies', sa.Column('recruiter_id', sa.Integer(), nullable=True))
    op.add_column('vacancies', sa.Column('hr_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'vacancies', 'users', ['hr_id'], ['id'])
    op.create_foreign_key(None, 'vacancies', 'users', ['recruiter_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vacancies', type_='foreignkey')
    op.drop_constraint(None, 'vacancies', type_='foreignkey')
    op.drop_column('vacancies', 'hr_id')
    op.drop_column('vacancies', 'recruiter_id')
    op.add_column('roadmaps', sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('roadmaps', sa.Column('deadline', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.alter_column('roadmaps', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('roadmaps', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('roadmaps', 'vacancy_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    op.alter_column('roadmaps', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('roadmaps_id_seq'::regclass)"))
    op.alter_column('roadmap_stages', 'duration',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('roadmap_stages', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('roadmap_stages', 'roadmap_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    op.alter_column('roadmap_stages', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_column('roadmap_stages', 'updated_at')
    op.drop_column('roadmap_stages', 'created_at')
    op.drop_column('roadmap_stages', 'order')
    op.drop_table('road_map_stage_completions')
    op.drop_table('candidate_skills')
    op.drop_table('candidates')
    # ### end Alembic commands ###
