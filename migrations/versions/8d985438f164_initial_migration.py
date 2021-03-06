"""Initial Migration.

Revision ID: 8d985438f164
Revises:
Create Date: 2019-04-20 02:27:25.030152

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8d985438f164"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Initial migration.

    Create the users and roles tables
    """
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("password", sa.Binary(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=True),
        sa.Column("last_name", sa.String(length=30), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Revert initial migration.

    Removes the roles and users tables.
    """
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("roles")
    op.drop_table("users")
    # ### end Alembic commands ###
