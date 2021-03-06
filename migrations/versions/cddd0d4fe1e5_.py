"""empty message

Revision ID: cddd0d4fe1e5
Revises: e3f21bc22405
Create Date: 2016-08-27 18:43:40.439148

"""

# revision identifiers, used by Alembic.
revision = 'cddd0d4fe1e5'
down_revision = 'e3f21bc22405'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('base_machine_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'course', 'machine', ['base_machine_id'], ['id'])
    op.alter_column('machine', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('user_courses', sa.Column('enabled', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_courses', 'enabled')
    op.alter_column('machine', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'base_machine_id')
    ### end Alembic commands ###
