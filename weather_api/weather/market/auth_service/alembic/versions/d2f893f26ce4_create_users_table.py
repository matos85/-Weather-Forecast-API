"""Create users table

Revision ID: d2f893f26ce4
Revises:
Create Date: 2025-04-08 19:36:42.355060

"""
from alembic import op
import sqlalchemy as sa

revision = 'd2f893f26ce4'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('patronymic', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('photo_path', sa.String(), nullable=True),
        sa.Column('telegram', sa.String(), nullable=True),
        sa.Column('registration_date', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login'),
        sa.UniqueConstraint('email')
    )

def downgrade() -> None:
    op.drop_table('users')