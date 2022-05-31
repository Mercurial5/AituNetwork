"""add education

Revision ID: 8693fa055c27
Revises: 840efe6f6a5e
Create Date: 2022-05-31 17:50:25.719304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8693fa055c27'
down_revision = '840efe6f6a5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('education', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'education')
    # ### end Alembic commands ###
