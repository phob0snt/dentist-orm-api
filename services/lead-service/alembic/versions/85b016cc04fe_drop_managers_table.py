"""Drop managers table

Revision ID: 85b016cc04fe
Revises: 955713d5d048
Create Date: 2025-07-29 12:51:53.022890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85b016cc04fe'
down_revision: Union[str, Sequence[str], None] = '955713d5d048'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("managers")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
