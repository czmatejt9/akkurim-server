"""add club table and profile pic for athletes

Revision ID: 7099f92a0135
Revises: b0096cbae295
Create Date: 2025-01-01 22:12:04.058144

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7099f92a0135"
down_revision: Union[str, None] = "b0096cbae295"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
        BEGIN;
        CREATE TABLE IF NOT EXISTS club (
            id text NOT NULL,
            name text NOT NULL,
            description text NOT NULL,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        );
        
        
        """
        )
    )


def downgrade() -> None:
    pass
