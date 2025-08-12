"""Construction Budget table

Revision ID: 456f78a4af12
Revises: b1024d92877f
Create Date: 2025-08-12 08:42:15.872943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '456f78a4af12'
down_revision: Union[str, Sequence[str], None] = 'b1024d92877f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add new IDENTITY column
    op.execute("""
        ALTER TABLE CONSTRUCTION_BUDGET ADD ID INT IDENTITY(1,1)
    """)

    # Step 2: Recreate primary key on new ID
    op.execute("""
        ALTER TABLE CONSTRUCTION_BUDGET ADD CONSTRAINT pk_CONSTRUCTION_BUDGET PRIMARY KEY (ID)
    """)


def downgrade():
    # Optional: reverse steps if needed
    pass
