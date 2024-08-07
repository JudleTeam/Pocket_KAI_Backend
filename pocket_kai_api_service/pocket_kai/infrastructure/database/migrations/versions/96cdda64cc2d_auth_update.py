"""Auth update

Revision ID: 96cdda64cc2d
Revises: 08f34ac73fe7
Create Date: 2024-07-12 15:25:40.262660

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '96cdda64cc2d'
down_revision: Union[str, None] = '08f34ac73fe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'refresh_token',
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('is_revoked', sa.Boolean(), nullable=False),
        sa.Column('issued_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
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
    )
    op.create_index(
        op.f('ix_refresh_token_token'),
        'refresh_token',
        ['token'],
        unique=True,
    )
    op.drop_table('token')
    op.create_unique_constraint(None, 'pocket_kai_user', ['phone'])
    op.drop_column('pocket_kai_user', 'last_activity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'pocket_kai_user',
        sa.Column(
            'last_activity',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(None, 'pocket_kai_user', type_='unique')
    op.create_table(
        'token',
        sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('pocket_kai_user_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            'id',
            sa.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['pocket_kai_user_id'],
            ['pocket_kai_user.id'],
            name='token_pocket_kai_user_id_fkey',
        ),
        sa.PrimaryKeyConstraint('id', name='token_pkey'),
        sa.UniqueConstraint('token', name='token_token_key'),
    )
    op.drop_index(op.f('ix_refresh_token_token'), table_name='refresh_token')
    op.drop_table('refresh_token')
    # ### end Alembic commands ###
