"""add server_default to created_at

Revision ID: 23c19ae3cb87
Revises: da71d97aaf87
Create Date: 2026-04-05 18:44:24.491545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23c19ae3cb87'
down_revision: Union[str, Sequence[str], None] = 'da71d97aaf87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('subscriptions', 'created_at', server_default=sa.text("now()"))
    op.alter_column('transactions', 'created_at', server_default=sa.text("now()"))


def downgrade() -> None:
    op.alter_column('subscriptions', 'created_at', server_default=None)
    op.alter_column('transactions', 'created_at', server_default=None)
