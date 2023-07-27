"""Adds API auth to connectors

Revision ID: c8c903153246
Revises: 7b25ec454c0a
Create Date: 2023-07-27 12:17:34.109626

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8c903153246"
down_revision = "7b25ec454c0a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("connectors_available", schema=None) as batch_op:
        batch_op.add_column(sa.Column("connector_accepts_api_key", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("connector_accepts_username_password", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("connector_accepts_file", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("connectors_available", schema=None) as batch_op:
        batch_op.drop_column("connector_accepts_file")
        batch_op.drop_column("connector_accepts_username_password")
        batch_op.drop_column("connector_accepts_api_key")

    # ### end Alembic commands ###
