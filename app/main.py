import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DB_CONNECTION_STRING="sqlite+pysqlite:///:memory:"

print(sqlalchemy.__version__)

engine = create_engine(DB_CONNECTION_STRING, echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello World!'"))
    print(result.all())

# "commit as you go"
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4},])
    conn.commit()

# "begin once"
with engine.begin() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 6, "y": 8}, {"x": 9, "y": 10},])

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    
    for row in result:
        print(f"x: {row.x} y: {row.y}")
        print(f"[]x: {row[0]} y: {row[1]}")

    result = conn.execute(text("SELECT x, y FROM some_table"))
    for x, y in result:
        print(f"x: {x} y: {y}")

    result = conn.execute(text("SELECT x, y FROM some_table"))
    for dict_row in result.mappings():
        print(f"x: {dict_row['x']} y: {dict_row['y']}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x} y: {row.y}")

with engine.connect() as conn:
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 11, "y":12}, {"x": 13, "y":14},])
        conn.commit()

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x} y: {row.y}")

with Session(engine) as session:
    result = session.execute(text("UPDATE some_table SET y=:y WHERE x=:x"), [{"x": 9, "y": 11}, {"x": 13, "y": 15} ,])
    session.commit()
