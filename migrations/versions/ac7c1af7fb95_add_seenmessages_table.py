"""add SeenMessages table

Revision ID: ac7c1af7fb95
Revises: f8690e5b3def
Create Date: 2022-07-15 16:25:35.765132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7c1af7fb95'
down_revision = 'f8690e5b3def'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seen_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seen_messages_message_id'), 'seen_messages', ['message_id'], unique=False)
    op.create_index(op.f('ix_seen_messages_user_id'), 'seen_messages', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_seen_messages_user_id'), table_name='seen_messages')
    op.drop_index(op.f('ix_seen_messages_message_id'), table_name='seen_messages')
    op.drop_table('seen_messages')
    # ### end Alembic commands ###
