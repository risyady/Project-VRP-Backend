"""empty message

Revision ID: dbb1fc8beb92
Revises: f2f682920492
Create Date: 2025-06-29 23:34:15.661579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbb1fc8beb92'
down_revision = 'f2f682920492'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=False, server_default=sa.true()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_user', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
