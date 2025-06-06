import uuid

from sqlalchemy import MetaData, Table, Column, String, DateTime, UUID, ForeignKey, Boolean, Integer, Text

convention = {
    'ix': 'ix_%(column_0_label)s',  # INDEX
    'uq': 'uq_%(table_name)s_%(column_0_N_name)s',  # UNIQUE
    'ck': 'ck_%(table_name)s_%(constraint_name)s',  # CHECK
    'fk': 'fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s',  # FOREIGN KEY
    'pk': 'pk_%(table_name)s',  # PRIMARY KEY
}


metadata = MetaData(naming_convention=convention)

users_table = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('is_admin', Boolean, default=False),
)


sessions_table = Table(
    'sessions',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('expired_at', DateTime, nullable=False),
)


news_table = Table(
    'news',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('text', Text, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('creator_id', UUID, ForeignKey('users.id'), nullable=False),
)


launchers_table = Table(
    'launchers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('version', String(255), nullable=False, unique=True),
    Column('created_at', DateTime, nullable=False),
    Column('creator_id', UUID, ForeignKey('users.id'), nullable=False),
    Column('file_path', String(255), nullable=False),
)


installers_table = Table(
    'installers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('version', String(255), nullable=False, unique=True),
    Column('created_at', DateTime, nullable=False),
    Column('creator_id', UUID, ForeignKey('users.id'), nullable=False),
    Column('file_path', String(255), nullable=False),
)
