"""empty message

Revision ID: c3c296380442
Revises: 74a331c948d6
Create Date: 2022-07-27 14:29:30.108799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c296380442'
down_revision = '74a331c948d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'lga', 'state', ['state_id'], ['state_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'lga', type_='foreignkey')
    # ### end Alembic commands ###
