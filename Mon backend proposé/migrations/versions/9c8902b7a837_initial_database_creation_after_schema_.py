"""Initial database creation after schema reset

Revision ID: 9c8902b7a837
Revises: 
Create Date: 2025-06-18 22:28:59.146799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c8902b7a837'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('role', sa.Enum('DRIVER', 'PASSENGER', name='userrole'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.Column('home_address', sa.String(length=255), nullable=True),
    sa.Column('habitual_departure_time', sa.String(length=50), nullable=True),
    sa.Column('habitual_arrival_time', sa.String(length=50), nullable=True),
    sa.Column('vehicle_make', sa.String(length=100), nullable=True),
    sa.Column('vehicle_model', sa.String(length=100), nullable=True),
    sa.Column('vehicle_seats_available', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('conversation_participants',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'conversation_id'),
    sa.UniqueConstraint('user_id', 'conversation_id', name='_user_conversation_uc')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('start_location', sa.String(length=255), nullable=False),
    sa.Column('end_location', sa.String(length=255), nullable=False),
    sa.Column('start_latitude', sa.Float(), nullable=True),
    sa.Column('start_longitude', sa.Float(), nullable=True),
    sa.Column('end_latitude', sa.Float(), nullable=True),
    sa.Column('end_longitude', sa.Float(), nullable=True),
    sa.Column('departure_time', sa.DateTime(), nullable=False),
    sa.Column('arrival_time_estimate', sa.DateTime(), nullable=True),
    sa.Column('recurring_days', sa.String(length=100), nullable=True),
    sa.Column('available_seats', sa.Integer(), nullable=False),
    sa.Column('price_per_passenger', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'COMPLETED', 'CANCELLED', name='tripstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('passenger_id', sa.Integer(), nullable=False),
    sa.Column('start_location', sa.String(length=255), nullable=False),
    sa.Column('end_location', sa.String(length=255), nullable=False),
    sa.Column('start_latitude', sa.Float(), nullable=True),
    sa.Column('start_longitude', sa.Float(), nullable=True),
    sa.Column('end_latitude', sa.Float(), nullable=True),
    sa.Column('end_longitude', sa.Float(), nullable=True),
    sa.Column('desired_departure_time', sa.DateTime(), nullable=False),
    sa.Column('desired_arrival_time_latest', sa.DateTime(), nullable=True),
    sa.Column('recurring_days', sa.String(length=100), nullable=True),
    sa.Column('number_of_passengers', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'COMPLETED', 'CANCELLED', name='tripstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['passenger_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('passenger_id', sa.Integer(), nullable=False),
    sa.Column('seats_booked', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['offer_id'], ['offers.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('requests')
    op.drop_table('offers')
    op.drop_table('messages')
    op.drop_table('conversation_participants')
    op.drop_table('users')
    op.drop_table('conversations')
    # ### end Alembic commands ###
