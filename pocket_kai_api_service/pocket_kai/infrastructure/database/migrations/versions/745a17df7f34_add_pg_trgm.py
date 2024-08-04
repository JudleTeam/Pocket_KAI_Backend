"""Add pg_trgm

Revision ID: 745a17df7f34
Revises: 9cbb5ab875f8
Create Date: 2024-08-04 15:18:02.741293

"""

from sqlalchemy import text
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '745a17df7f34'
down_revision: Union[str, None] = '9cbb5ab875f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(text('DROP EXTENSION IF EXISTS pg_trgm'))
    # ### end Alembic commands ###