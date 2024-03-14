from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

DB_CONNECTION_STRING="sqlite+pysqlite:///:memory:"

engine = create_engine(DB_CONNECTION_STRING, echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

print(user_table.c.name)

print(user_table.c.keys())

print(user_table.primary_key)

address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey("user_account.id"), nullable=False),
    Column('email_address', String, nullable=False),
)

metadata_obj.create_all(engine)