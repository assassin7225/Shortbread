"""empty message

Revision ID: 22b85662d879
Revises: 
Create Date: 2018-06-07 01:35:33.754347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b85662d879'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URLData',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('OriginURL', sa.String(length=256), nullable=True),
    sa.Column('ShortURL', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('URLData')
    # ### end Alembic commands ###
