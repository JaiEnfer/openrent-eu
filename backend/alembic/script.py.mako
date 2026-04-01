"""
Revision script template for Alembic (default).
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "${up_revision}"
down_revision = ${down_revision}
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
