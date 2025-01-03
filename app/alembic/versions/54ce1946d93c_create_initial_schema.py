"""create initial schema

Revision ID: 54ce1946d93c
Revises:
Create Date: 2024-12-31 14:53:10.396389

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "54ce1946d93c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open("/app/app/resources/sql/schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    conn = op.get_bind()
    conn.execute(sa.text(sql))


def downgrade() -> None:
    pass
