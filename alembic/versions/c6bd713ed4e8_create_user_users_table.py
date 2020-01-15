"""Create user users table

Revision ID: c6bd713ed4e8
Revises:
Create Date: 2020-01-09 17:48:06.605084

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6bd713ed4e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.now),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now),
    )


def downgrade():
    op.drop_table('user_users')
