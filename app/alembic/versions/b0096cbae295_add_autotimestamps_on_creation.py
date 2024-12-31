"""add autotimestamps on creation

Revision ID: b0096cbae295
Revises: 54ce1946d93c
Create Date: 2025-01-01 00:28:49.400987

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b0096cbae295"
down_revision: Union[str, None] = "54ce1946d93c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        BEGIN;

        -- Alter `created_at` and `updated_at` columns for each table

        ALTER TABLE guardian
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE item
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE athlete
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE trainer
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE web_post
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE "group"
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE training
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE sign_up_form
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE meet
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE meet_event
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        ALTER TABLE athlete_meet_event
            ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

        -- Add more tables if needed

        COMMIT;

        """
    )


def downgrade() -> None:
    pass
