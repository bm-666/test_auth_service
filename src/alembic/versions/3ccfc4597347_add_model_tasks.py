"""add model tasks

Revision ID: 3ccfc4597347
Revises: 1fab16834757
Create Date: 2025-05-11 14:41:36.933774

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "3ccfc4597347"
down_revision: Union[str, None] = "1fab16834757"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
