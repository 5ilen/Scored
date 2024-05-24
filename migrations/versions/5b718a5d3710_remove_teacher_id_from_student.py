"""Remove teacher_id from Student

Revision ID: 5b718a5d3710
Revises: 3350c6047c25
Create Date: 2024-05-24 22:30:00.112233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b718a5d3710'
down_revision = '3350c6047c25'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.drop_constraint('fk_student_user', type_='foreignkey')
        batch_op.drop_column('teacher_id')
        batch_op.create_foreign_key('fk_student_user', 'user', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.add_column(sa.Column('teacher_id', sa.Integer, nullable=True))
        batch_op.create_foreign_key('fk_student_user', 'user', ['user_id'], ['id'])
