"""init

Revision ID: 1353a33ea79b
Revises:
Create Date: 2024-04-29 17:41:20.250462

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1353a33ea79b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'department',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'discipline',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'profile',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'speciality',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'institute',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'pocket_kai_user',
        sa.Column('telegram_id', sa.BigInteger(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('is_blocked', sa.Boolean(), nullable=False),
        sa.Column('last_activity', sa.DateTime(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id'),
    )

    op.create_table(
        'group',
        sa.Column('kai_id', sa.BigInteger(), nullable=False),
        sa.Column('group_leader_id', sa.Uuid(), nullable=True),
        sa.Column('pinned_text', sa.String(), nullable=True),
        sa.Column('group_name', sa.String(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('parsed_at', sa.DateTime(), nullable=True),
        sa.Column('syllabus_url', sa.String(), nullable=True),
        sa.Column('educational_program_url', sa.String(), nullable=True),
        sa.Column('study_schedule_url', sa.String(), nullable=True),
        sa.Column('speciality_id', sa.Uuid(), nullable=True),
        sa.Column('profile_id', sa.Uuid(), nullable=True),
        sa.Column('institute_id', sa.Uuid(), nullable=True),
        sa.Column('department_id', sa.Uuid(), nullable=True),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['department.id']),
        sa.ForeignKeyConstraint(['institute_id'], ['institute.id']),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id']),
        sa.ForeignKeyConstraint(['speciality_id'], ['speciality.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('group_name'),
        sa.UniqueConstraint('kai_id'),
    )

    op.create_table(
        'kai_user',
        sa.Column('kai_id', sa.BigInteger(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('login', sa.String(), nullable=True),
        sa.Column(
            'password',
            sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(),
            nullable=True,
        ),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('sex', sa.String(), nullable=True),
        sa.Column('birthday', sa.Date(), nullable=True),
        sa.Column('is_leader', sa.Boolean(), nullable=False),
        sa.Column('zach_number', sa.String(), nullable=True),
        sa.Column('competition_type', sa.String(), nullable=True),
        sa.Column('contract_number', sa.BigInteger(), nullable=True),
        sa.Column('edu_level', sa.String(), nullable=True),
        sa.Column('edu_cycle', sa.String(), nullable=True),
        sa.Column('edu_qualification', sa.String(), nullable=True),
        sa.Column('program_form', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('group_id', sa.Uuid(), nullable=False),
        sa.Column('pocket_kai_user_id', sa.Uuid(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['pocket_kai_user_id'], ['pocket_kai_user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('kai_id'),
        sa.UniqueConstraint('login'),
        sa.UniqueConstraint('pocket_kai_user_id'),
    )

    op.create_foreign_key(
        'fk_kai_user_group',
        'kai_user',
        'group',
        ['group_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_group_kai_user',
        'group',
        'kai_user',
        ['group_leader_id'],
        ['id'],
    )

    op.create_table(
        'teacher',
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('departament_id', sa.Uuid(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['departament_id'], ['department.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login'),
    )

    op.create_table(
        'token',
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('pocket_kai_user_id', sa.Uuid(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['pocket_kai_user_id'], ['pocket_kai_user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token'),
    )

    op.create_table(
        'group_lesson',
        sa.Column('number_of_day', sa.Integer(), nullable=False),
        sa.Column('original_dates', sa.String(), nullable=True),
        sa.Column('parsed_parity', sa.String(), nullable=False),
        sa.Column('parsed_dates', sa.ARRAY(sa.Date()), nullable=True),
        sa.Column('audience_number', sa.String(), nullable=True),
        sa.Column('building_number', sa.String(), nullable=True),
        sa.Column('original_lesson_type', sa.String(), nullable=True),
        sa.Column('parsed_lesson_type', sa.String(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('discipline_id', sa.Uuid(), nullable=False),
        sa.Column('teacher_id', sa.Uuid(), nullable=True),
        sa.Column('group_id', sa.Uuid(), nullable=False),
        sa.Column('parsed_at', sa.DateTime(), nullable=False),
        sa.Column(
            'id',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['discipline_id'], ['discipline.id']),
        sa.ForeignKeyConstraint(['group_id'], ['group.id']),
        sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_lesson')
    op.drop_table('token')
    op.drop_table('teacher')
    op.drop_table('speciality')
    op.drop_table('profile')
    op.drop_table('pocket_kai_user')
    op.drop_table('kai_user')
    op.drop_table('institute')
    op.drop_table('group')
    op.drop_table('discipline')
    op.drop_table('department')
    # ### end Alembic commands ###
