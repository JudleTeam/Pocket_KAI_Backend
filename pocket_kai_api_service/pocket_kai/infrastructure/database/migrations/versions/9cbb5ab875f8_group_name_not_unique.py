"""Group name not unique

Revision ID: 9cbb5ab875f8
Revises: 1be16526ac45
Create Date: 2024-07-29 10:45:33.710396

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9cbb5ab875f8'
down_revision: Union[str, None] = '1be16526ac45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('group_group_name_key', 'group', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('group_group_name_key', 'group', ['group_name'])
    # ### end Alembic commands ###