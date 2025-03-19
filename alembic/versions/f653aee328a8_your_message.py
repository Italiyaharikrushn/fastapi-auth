"""your message

Revision ID: f653aee328a8
Revises: 7c9b4de4903a
Create Date: 2025-03-19 12:09:32.979427

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f653aee328a8'
down_revision = '7c9b4de4903a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    op.add_column('user', sa.Column('role', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.create_table('document',
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('modified_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('status', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('static_file_path', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('actual_file_path', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('modified_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='document_created_by_fkey'),
    sa.ForeignKeyConstraint(['modified_by'], ['user.id'], name='document_modified_by_fkey'),
    sa.PrimaryKeyConstraint('id', name='document_pkey')
    )
    # ### end Alembic commands ###
