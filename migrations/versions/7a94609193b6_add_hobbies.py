"""add hobbies

Revision ID: 7a94609193b6
Revises: 8693fa055c27
Create Date: 2022-05-31 18:10:59.962858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a94609193b6'
down_revision = '8693fa055c27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hobbies', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'hobbies')
    # ### end Alembic commands ###