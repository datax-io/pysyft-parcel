"""
Adds privacy budget column 'budget' to syft_user

Revision ID: cd246fe6ff78
Revises: 0cda31d54345
Create Date: 2021-08-30 13:33:14.867786

"""
# third party
from alembic import op  # type: ignore
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "cd246fe6ff78"
down_revision = "0cda31d54345"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("syft_user", sa.Column("budget", sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("syft_user", "budget")
    # ### end Alembic commands ###
