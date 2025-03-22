"""Make shipping fields nullable

Revision ID: 784fdb532303
Revises: cd45d0e0f481
Create Date: 2025-03-22 12:24:07.614373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '784fdb532303'
down_revision = 'cd45d0e0f481'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('billing_addresses', 'billing_address',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('billing_addresses', 'billing_state',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_fullname',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('billing_addresses', 'shipping_address',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               nullable=True)
    op.alter_column('billing_addresses', 'shipping_city',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('billing_addresses', 'shipping_pincode',
               existing_type=sa.VARCHAR(length=6),
               nullable=True)
    op.alter_column('billing_addresses', 'shipping_country',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('billing_addresses', 'shipping_contact_number',
               existing_type=sa.VARCHAR(length=14),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('billing_addresses', 'shipping_contact_number',
               existing_type=sa.VARCHAR(length=14),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_country',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_pincode',
               existing_type=sa.VARCHAR(length=6),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_city',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_address',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=False)
    op.alter_column('billing_addresses', 'shipping_fullname',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('billing_addresses', 'billing_state',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('billing_addresses', 'billing_address',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###
