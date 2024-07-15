"""Fix kai user model

Revision ID: 9243bc42daa6
Revises: 96cdda64cc2d
Create Date: 2024-07-12 15:28:57.322617

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9243bc42daa6'
down_revision: Union[str, None] = '96cdda64cc2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'kai_user',
        'contract_number',
        existing_type=sa.BIGINT(),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'kai_user',
        'contract_number',
        existing_type=sa.String(),
        type_=sa.BIGINT(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###