"""add photo to user

Revision ID: c0e0262ad4ec
Revises: 5484b8078426
Create Date: 2023-02-23 18:56:51.415827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0e0262ad4ec'
down_revision = '5484b8078426'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('photo', sa.String(length=55), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'photo')
    # ### end Alembic commands ###
