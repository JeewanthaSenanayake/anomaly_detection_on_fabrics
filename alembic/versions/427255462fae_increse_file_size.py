"""increse file size

Revision ID: 427255462fae
Revises: 2db71fa5bcd6
Create Date: 2024-07-09 08:56:18.412548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '427255462fae'
down_revision: Union[str, None] = '2db71fa5bcd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
