"""create_psot_table

Revision ID: fe2f584c308f
Revises: 
Create Date: 2023-06-19 12:38:00.245716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe2f584c308f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key = True, nullable = False),
                            sa.Column('title', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_table('posts')
    pass
