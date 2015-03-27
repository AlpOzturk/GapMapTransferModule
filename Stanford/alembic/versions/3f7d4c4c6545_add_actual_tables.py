"""Add actual tables

Revision ID: 3f7d4c4c6545
Revises: 5183cc749c7c
Create Date: 2015-03-26 15:51:37.407000

"""

# revision identifiers, used by Alembic.
revision = '3f7d4c4c6545'
down_revision = '5183cc749c7c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa




def upgrade():
    op.drop_table('test')
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('second_name', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('contactable', sa.Boolean, default=False),
        sa.Column('subscribable', sa.Boolean, default=False),
        sa.Column('date', sa.Date),
        sa.Column('last_updated', sa.DateTime)
    )
    op.create_table(
        'participants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('contact_id', sa.Integer, nullable=False),
        sa.Column('birthday', sa.Date),
        sa.Column('gender', sa.String(255)),
        sa.Column('diagnosis', sa.String(255)),
        sa.Column('diagnosis_date', sa.Date),
        sa.Column('ados', sa.Boolean),
        sa.Column('adir', sa.Boolean),
        sa.Column('other_diagnosis_tool', sa.String(255)),
        sa.Column('city', sa.String(255)),
        sa.Column('state', sa.String(255)),
        sa.Column('country', sa.String(255)),
        sa.Column('zip_code', sa.Integer),
        sa.Column('latitude', sa.Float),
        sa.Column('longitude', sa.Float),
        sa.Column('last_updated', sa.DateTime)
    )


def downgrade():
    op.drop_table('contacts')
    op.drop_table('participants')
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False)
    )
