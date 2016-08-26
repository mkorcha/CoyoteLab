"""empty message

Revision ID: e3f21bc22405
Revises: 8e10975ee6b1
Create Date: 2016-08-26 14:58:51.390137

"""

# revision identifiers, used by Alembic.
revision = 'e3f21bc22405'
down_revision = '8e10975ee6b1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('machine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('base_machine_id', sa.Integer(), nullable=True),
    sa.Column('last_active', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['base_machine_id'], ['machine.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('machine')
    ### end Alembic commands ###
