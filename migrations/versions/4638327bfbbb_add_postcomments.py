"""add postComments

Revision ID: 4638327bfbbb
Revises: c5aaa2a7ff68
Create Date: 2022-06-01 10:56:35.646290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4638327bfbbb'
down_revision = 'c5aaa2a7ff68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_comments_comment_id'), 'post_comments', ['comment_id'], unique=False)
    op.create_index(op.f('ix_post_comments_post_id'), 'post_comments', ['post_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_comments_post_id'), table_name='post_comments')
    op.drop_index(op.f('ix_post_comments_comment_id'), table_name='post_comments')
    op.drop_table('post_comments')
    # ### end Alembic commands ###
