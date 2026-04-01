"""baseline: create tables from models

Revision ID: 0001_initial_baseline
Revises: 
Create Date: 2026-04-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_baseline'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Import application metadata and create all tables as baseline
    from app.core.db import engine, Base
    Base.metadata.create_all(bind=engine)


def downgrade() -> None:
    # Drop all tables (careful: destructive)
    from app.core.db import engine, Base
    Base.metadata.drop_all(bind=engine)
