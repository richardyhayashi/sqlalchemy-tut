from sqlalchemy import create_engine, insert, select, bindparam, \
                       MetaData, Table, Column, Integer, String, ForeignKey

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

stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")

print(stmt)

compiled = stmt.compile()

print(compiled.params)

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
    
    print(result.inserted_primary_key)

print(insert(user_table))

with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()


scalar_subq = (
    select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
)

with engine.connect() as conn:
    result = conn.execute(
        insert(address_table).values(user_id=scalar_subq),
        [
            {
                "username": "spongebob",
                "email_address": "spongebob@sqlalchemy.org",
            },
            {
                "username": "sandy",
                "email_address": "sandy@sqlalchemy.org"
            },
            {
                "username": "sandy",
                "email_address": "sandy@squirrelpower.org"
            },
        ],
    )
    conn.commit()

print(insert(user_table).values().compile(engine))

insert_stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)

print(insert_stmt)

select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")

insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)

print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))

select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")

insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)

print(insert_stmt)

stmt = select(user_table).where(user_table.c.name == "spongebob")

print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

print(select(user_table))

print(select(user_table.c.name, user_table.c.fullname))