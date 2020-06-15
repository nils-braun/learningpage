"""Inital commit

Revision ID: a90368071bc4
Revises: 
Create Date: 2020-06-14 19:12:33.616185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a90368071bc4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "courses",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("access_string", sa.String(), nullable=False),
        sa.Column("sort_number", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "instructors",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "skills",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "content_groups",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("course_slug", sa.String(length=32), nullable=False),
        sa.Column("sort_number", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["course_slug"], ["courses.slug"],),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "contents",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("subtitle", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("learnings", sa.String(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("content_group_slug", sa.String(length=32), nullable=False),
        sa.Column("sort_number", sa.Integer(), nullable=False),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("assignment_slug", sa.String(), nullable=True),
        sa.Column("git_url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["content_group_slug"], ["content_groups.slug"],),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "content_instructor_association",
        sa.Column("content_slug", sa.String(length=32), nullable=False),
        sa.Column("instructor_slug", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["content_slug"], ["contents.slug"],),
        sa.ForeignKeyConstraint(["instructor_slug"], ["instructors.slug"],),
    )
    op.create_table(
        "content_skill_association",
        sa.Column("content_slug", sa.String(length=32), nullable=False),
        sa.Column("skill_slug", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["content_slug"], ["contents.slug"],),
        sa.ForeignKeyConstraint(["skill_slug"], ["skills.slug"],),
    )
    op.create_table(
        "facts",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("extra", sa.JSON(), nullable=False),
        sa.Column("content_slug", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["content_slug"], ["contents.slug"],),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "submissions",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("content_slug", sa.String(length=32), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("user", sa.String(), nullable=False),
        sa.Column("external_identifier", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["content_slug"], ["contents.slug"],),
        sa.PrimaryKeyConstraint("slug"),
    )
    op.create_table(
        "notebooks",
        sa.Column("slug", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("submission_slug", sa.String(length=32), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("max_score", sa.Float(), nullable=False),
        sa.Column("graded", sa.Boolean(), server_default="f", nullable=False),
        sa.ForeignKeyConstraint(["submission_slug"], ["submissions.slug"],),
        sa.PrimaryKeyConstraint("slug"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notebooks")
    op.drop_table("submissions")
    op.drop_table("facts")
    op.drop_table("content_skill_association")
    op.drop_table("content_instructor_association")
    op.drop_table("contents")
    op.drop_table("content_groups")
    op.drop_table("skills")
    op.drop_table("instructors")
    op.drop_table("courses")
    # ### end Alembic commands ###