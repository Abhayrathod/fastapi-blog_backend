"""add content column to posts table

Revision ID: 427b0b33ad7f
Revises: 564cbb3a000b
Create Date: 2022-08-14 15:37:14.092508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427b0b33ad7f'
down_revision = '564cbb3a000b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
