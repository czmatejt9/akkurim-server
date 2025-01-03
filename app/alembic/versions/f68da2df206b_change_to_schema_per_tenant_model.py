"""change to schema per tenant model

Revision ID: f68da2df206b
Revises: 7099f92a0135
Create Date: 2025-01-03 09:54:29.096041

"""

import re
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f68da2df206b"
down_revision: Union[str, None] = "7099f92a0135"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open("/app/app/resources/sql/updated_schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    with open("/app/app/resources/sql/active_tenants.sql", "r", encoding="utf-8") as f:
        tenants = [each for each in f.read().split("\n") if each]

    conn = op.get_bind()
    # drop all old tables
    conn.execute(sa.text("DROP SCHEMA public CASCADE;"))
    conn.execute(sa.text("CREATE SCHEMA public;"))

    for tenant_id in tenants:
        sql = re.sub("tenant_id", tenant_id, sql)
        conn.execute(sa.text(sql))


def downgrade() -> None:
    pass