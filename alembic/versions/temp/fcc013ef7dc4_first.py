"""first

Revision ID: fcc013ef7dc4
Revises: 
Create Date: 2022-03-15 12:26:18.284082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcc013ef7dc4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('status', sa.Boolean(), nullable=True))
    op.execute("UPDATE movie SET status = True")
    op.alter_column('movie', 'status', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'status')
    # ### end Alembic commands ###