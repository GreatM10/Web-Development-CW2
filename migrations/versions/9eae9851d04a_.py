"""empty message

Revision ID: 9eae9851d04a
Revises: 
Create Date: 2022-12-13 16:20:08.434883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eae9851d04a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_name', sa.String(length=64), nullable=True),
    sa.Column('activity_info', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('limit', sa.Integer(), nullable=True),
    sa.Column('applied', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity_user',
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('activity_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activity_user')
    op.drop_table('user')
    op.drop_table('admin')
    op.drop_table('activity')
    # ### end Alembic commands ###
