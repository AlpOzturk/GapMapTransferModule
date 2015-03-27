"""Test table

Revision ID: 5183cc749c7c
Revises: 
Create Date: 2015-03-25 03:08:12.247000

"""

# revision identifiers, used by Alembic.
revision = '5183cc749c7c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False)
    )


def downgrade():
    op.drop_table('test')
