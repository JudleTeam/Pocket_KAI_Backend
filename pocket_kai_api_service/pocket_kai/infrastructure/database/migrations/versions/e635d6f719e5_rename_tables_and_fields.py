"""Rename tables and fields

Revision ID: e635d6f719e5
Revises: b13615cb75b1
Create Date: 2024-07-13 10:05:00.393939

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e635d6f719e5'
down_revision: Union[str, None] = 'b13615cb75b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('kai_user', 'student')
    op.rename_table('group_lesson', 'lesson')
    op.rename_table('pocket_kai_user', 'user')

    op.alter_column('student', 'pocket_kai_user_id', new_column_name='user_id')
    op.drop_constraint('kai_user_pocket_kai_user_id_key', 'student', type_='unique')
    op.drop_constraint(
        'kai_user_pocket_kai_user_id_fkey',
        'student',
        type_='foreignkey',
    )
    op.create_foreign_key(None, 'student', 'user', ['user_id'], ['id'])
    op.create_unique_constraint(None, 'student', ['user_id'])

    op.drop_constraint('fk_group_kai_user', 'group', type_='foreignkey')
    op.create_foreign_key(None, 'group', 'student', ['group_leader_id'], ['id'])

    op.alter_column('refresh_token', 'pocket_kai_user_id', new_column_name='user_id')
    op.drop_constraint(
        'refresh_token_pocket_kai_user_id_fkey',
        'refresh_token',
        type_='foreignkey',
    )
    op.create_foreign_key(None, 'refresh_token', 'user', ['user_id'], ['id'])


def downgrade() -> None:
    op.rename_table('student', 'kai_user')
    op.rename_table('lesson', 'group_lesson')
    op.rename_table('user', 'pocket_kai_user')

    op.alter_column('student', 'user_id', new_column_name='pocket_kai_user_id')
    op.drop_constraint('student_user_id_fkey', 'kai_user', type_='foreignkey')
    op.drop_constraint('student_user_id_key', 'kai_user', type_='unique')
    op.create_foreign_key(
        None,
        'kai_user',
        'pocket_kai_user',
        ['pocket_kai_user_id'],
        ['id'],
    )
    op.create_unique_constraint(None, 'student', ['pocket_kai_user_id'])

    op.drop_constraint('group_group_leader_id_fkey', 'group_lesson', type_='foreignkey')
    op.create_foreign_key(None, 'group_lesson', 'kai_user', ['group_leader_id'], ['id'])

    op.alter_column('refresh_token', 'user_id', new_column_name='pocket_kai_user_id')
    op.drop_constraint(
        'refresh_token_user_id_fkey',
        'refresh_token',
        type_='foreignkey',
    )
    op.create_foreign_key(
        None,
        'refresh_token',
        'pocket_kai_user',
        ['pocket_kai_user_id'],
        ['id'],
    )
