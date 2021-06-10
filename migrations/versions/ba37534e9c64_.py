"""empty message

Revision ID: ba37534e9c64
Revises: 9941ac5caceb
Create Date: 2021-06-07 18:57:25.644862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba37534e9c64'
down_revision = '9941ac5caceb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
