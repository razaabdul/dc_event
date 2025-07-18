"""Added event_date, service, budget to contact

Revision ID: ed3ce48ab517
Revises: c9964708ec1c
Create Date: 2025-07-15 13:31:06.678763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed3ce48ab517'
down_revision = 'c9964708ec1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('service', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('budget', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.drop_column('budget')
        batch_op.drop_column('service')
        batch_op.drop_column('event_date')

    # ### end Alembic commands ###
