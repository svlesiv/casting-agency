"""empty message

Revision ID: e6699c62a6e1
Revises: 
Create Date: 2021-09-25 16:34:05.804084

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e6699c62a6e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.alter_column('movies', 'release_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'release_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###
