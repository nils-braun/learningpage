"""Changed name of instructor.logo_url to image_url

Revision ID: ea61fad81ba8
Revises: 0cc65d758c8c
Create Date: 2020-05-07 21:29:36.841060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ea61fad81ba8"
down_revision = "0cc65d758c8c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("instructors", "logo_url", new_column_name="image_url")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("instructors", "image_url", new_column_name="logo_url")
    # ### end Alembic commands ###
