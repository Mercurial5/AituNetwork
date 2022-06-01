"""add cities

Revision ID: 3c5c22b7ee64
Revises: c70b18dfbcfe
Create Date: 2022-06-01 04:21:04.552149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c5c22b7ee64'
down_revision = 'c70b18dfbcfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    cities = sa.sql.table('cities',
                          sa.sql.column('id', sa.Integer),
                          sa.sql.column('name', sa.String))

    op.bulk_insert(cities, [
        {'name': 'Aktau'},
        {'name': 'Aktobe'},
        {'name': 'Almaty'},
        {'name': 'Arkalyk'},
        {'name': 'Atyrau'},
        {'name': 'Baikonur'},
        {'name': 'Balqash'},
        {'name': 'Zhezkazgan'},
        {'name': 'Karaganda'},
        {'name': 'Kentau'},
        {'name': 'Kyzylorda'},
        {'name': 'Kokshetau'},
        {'name': 'Kostanay'},
        {'name': 'Nur-Sultan'},
        {'name': 'Zhanaozen'},
        {'name': 'Pavlodar'},
        {'name': 'Petropavl'},
        {'name': 'Ridder'},
        {'name': 'Saran'},
        {'name': 'Satpayev'},
        {'name': 'Semey'},
        {'name': 'Stepnogorsk'},
        {'name': 'Taldykorgan'},
        {'name': 'Taraz'},
        {'name': 'Temirtau'},
        {'name': 'Turkistan'},
        {'name': 'Oral'},
        {'name': 'Oskemen'},
        {'name': 'Shymkent'},
        {'name': 'Shakhtinsk'},
        {'name': 'Schuchinsk'},
        {'name': 'Ekibastuz'},
    ])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cities')
    # ### end Alembic commands ###
