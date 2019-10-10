"""Account :  calcul agios en cours de test

Revision ID: 48256c506d42
Revises: 0a5931f71bac
Create Date: 2019-10-10 19:01:11.464465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48256c506d42'
down_revision = '0a5931f71bac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'account', 'client', ['client_id'], ['id'])
    op.create_foreign_key(None, 'admin', 'user', ['id'], ['id'])
    op.create_foreign_key(None, 'client', 'manager', ['manager_id'], ['manager_id'])
    op.create_foreign_key(None, 'client', 'user', ['id'], ['id'])
    op.create_foreign_key(None, 'debit_account_agios_history', 'account', ['account_id'], ['id'])
    op.create_foreign_key(None, 'manager', 'user', ['id'], ['id'])
    op.create_foreign_key(None, 'paid_account_benefit_history', 'account', ['account_id'], ['id'])
    op.create_foreign_key(None, 'transaction_history', 'account', ['account_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction_history', type_='foreignkey')
    op.drop_constraint(None, 'paid_account_benefit_history', type_='foreignkey')
    op.drop_constraint(None, 'manager', type_='foreignkey')
    op.drop_constraint(None, 'debit_account_agios_history', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_constraint(None, 'admin', type_='foreignkey')
    op.drop_constraint(None, 'account', type_='foreignkey')
    # ### end Alembic commands ###
