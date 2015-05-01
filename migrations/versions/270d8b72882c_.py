"""empty message

Revision ID: 270d8b72882c
Revises: 4ddc00c7d2ba
Create Date: 2015-04-30 16:01:02.220171

"""

# revision identifiers, used by Alembic.
revision = '270d8b72882c'
down_revision = '4ddc00c7d2ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scores',
    sa.Column('problemset_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['problemset_id'], ['problemset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column(u'category', sa.Column('problems_count', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.add_column(u'problemset', sa.Column('problems_count', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'problemset', 'problems_count')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_column(u'category', 'problems_count')
    op.drop_table('scores')
    ### end Alembic commands ###