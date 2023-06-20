"""addphonenumber

Revision ID: e9839b11f7d3
Revises: 9e201832fda5
Create Date: 2023-06-19 15:41:46.139384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9839b11f7d3'
down_revision = '9e201832fda5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
