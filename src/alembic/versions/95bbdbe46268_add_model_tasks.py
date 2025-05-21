"""add model tasks

Revision ID: 95bbdbe46268
Revises: 3ccfc4597347
Create Date: 2025-05-12 06:28:44.380917

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "95bbdbe46268"
down_revision: Union[str, None] = "3ccfc4597347"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
