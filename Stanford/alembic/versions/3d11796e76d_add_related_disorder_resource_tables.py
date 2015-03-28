"""Add related disorder & resource tables

Revision ID: 3d11796e76d
Revises: 3f7d4c4c6545
Create Date: 2015-03-27 15:47:01.451000

"""

# revision identifiers, used by Alembic.
revision = '3d11796e76d'
down_revision = '3f7d4c4c6545'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table(
        'resources',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('resource', sa.String(255))
    )

    op.create_table(
        'related_disorders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('disorder', sa.String(255))
    )

    op.create_table(
        'participant_resources',
        sa.Column('participant_id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('resource_id', sa.Integer, primary_key=True, nullable=False)
    )

    op.create_table(
        'participant_related_disorders',
        sa.Column('participant_id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('disorder_id', sa.Integer, primary_key=True, nullable=False)
    )



def downgrade():
    op.drop_table('resources')
    op.drop_table('related_disorders')
    op.drop_table('participant_resources')
    op.drop_table('participant_related_disorders')
