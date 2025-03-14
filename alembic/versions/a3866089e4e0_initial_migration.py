"""Initial migration

Revision ID: a3866089e4e0
Revises: 
Create Date: 2025-03-12 14:40:05.080163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3866089e4e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=8), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('modified_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_email'), 'client', ['email'], unique=True)
    op.create_index(op.f('ix_client_id'), 'client', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=15), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('is_super_admin', sa.Boolean(), nullable=False),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('role', sa.Enum('SELLER', 'ADMIN', 'CUSTOMER', name='roleenum'), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('modified_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index(op.f('ix_client_id'), table_name='client')
    op.drop_index(op.f('ix_client_email'), table_name='client')
    op.drop_table('client')
    # ### end Alembic commands ###
