"""empty message

Revision ID: 1837339e5be0
Revises: 1c6fb0f47bd1
Create Date: 2019-10-09 12:03:51.839591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1837339e5be0'
down_revision = '1c6fb0f47bd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'admin', 'user', ['id'], ['id'])
    op.create_foreign_key(None, 'client', 'user', ['id'], ['id'])
    op.create_foreign_key(None, 'client', 'manager', ['manager_id'], ['manager_id'])
    op.create_foreign_key(None, 'manager', 'user', ['id'], ['id'])
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_column('user', 'username')
    op.drop_constraint(None, 'manager', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_constraint(None, 'admin', type_='foreignkey')
    # ### end Alembic commands ###
