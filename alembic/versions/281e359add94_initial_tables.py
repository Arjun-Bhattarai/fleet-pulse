"""initial tables

Revision ID: 281e359add94
Revises: a63c9589b78b
Create Date: 2026-05-08 16:18:39.506611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '281e359add94'
down_revision: Union[str, Sequence[str], None] = 'a63c9589b78b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
