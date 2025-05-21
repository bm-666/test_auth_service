"""

Revision ID: adbdb4f0b577
Revises: 95bbdbe46268
Create Date: 2025-05-12 13:49:26.916615

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "adbdb4f0b577"
down_revision: Union[str, None] = "95bbdbe46268"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
