"""add sequence and default constraint for id auto-increment on SQL Server

Revision ID: 93875bdac5a3
Revises: 64cf8d16160c
Create Date: 2025-07-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '93875bdac5a3'
down_revision = '64cf8d16160c'
branch_labels = None
depends_on = None



def upgrade():
    # Step 1: Add new IDENTITY column
    op.execute("""
        ALTER TABLE OPERATING_BUDGET ADD ID_NEW INT IDENTITY(1,1)
    """)

    # Step 2: Drop old PK constraint
    op.execute("""
        ALTER TABLE OPERATING_BUDGET DROP CONSTRAINT pk_OPERATING_BUDGET
    """)

    # Step 3: Drop old ID column
    op.execute("""
        ALTER TABLE OPERATING_BUDGET DROP COLUMN ID
    """)

    # Step 4: Rename ID_NEW to ID
    op.execute("""
        EXEC sp_rename 'OPERATING_BUDGET.ID_NEW', 'ID', 'COLUMN'
    """)

    # Step 5: Recreate primary key on new ID
    op.execute("""
        ALTER TABLE OPERATING_BUDGET ADD CONSTRAINT pk_OPERATING_BUDGET PRIMARY KEY (ID)
    """)


def downgrade():
    # Revert changes: optional
    pass