"""Add user_id to Student

Revision ID: 3350c6047c25
Revises: fb487b9b05dd
Create Date: 2024-05-24 21:56:34.112233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3350c6047c25'
down_revision = 'fb487b9b05dd'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_student_user', 'user', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.drop_constraint('fk_student_user', type_='foreignkey')
        batch_op.drop_column('user_id')