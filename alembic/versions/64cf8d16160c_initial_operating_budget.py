"""Initial Operating Budget

Revision ID: 64cf8d16160c
Revises: 
Create Date: 2025-07-07 08:35:21.752574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer


# revision identifiers, used by Alembic.
revision: str = '64cf8d16160c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'OPERATING_BUDGET',
        sa.Column('id', sa.Integer(), nullable=True)
    )

    op.execute("""
        WITH CTE AS (
            SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn, *
            FROM OPERATING_BUDGET
        )
        UPDATE CTE
        SET id = rn;
    """)

    op.alter_column(
        'OPERATING_BUDGET',
        'id',
        existing_type=sa.Integer(),
        nullable=False
    )

    op.create_primary_key('pk_OPERATING_BUDGET', 'OPERATING_BUDGET', ['id'])

def downgrade():
    op.drop_constraint('pk_OPERATING_BUDGET', 'OPERATING_BUDGET', type_='primary')
    op.drop_column('OPERATING_BUDGET', 'id')
