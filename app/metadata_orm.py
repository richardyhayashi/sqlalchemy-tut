from typing import List, Optional
from sqlalchemy import create_engine, String, ForeignKey, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

DB_CONNECTION_STRING="sqlite+pysqlite:///:memory:"

engine = create_engine(DB_CONNECTION_STRING, echo=True)

class Base(DeclarativeBase):
    pass

print(Base.metadata)

print(Base.registry)

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
    
Base.metadata.create_all(engine)


# ***INSERT***

stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")

print(stmt)

compiled = stmt.compile()

print(compiled.params)

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
    
    print(result.inserted_primary_key)


stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

with engine.connect() as conn:
    result = conn.execute(
        insert(User),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()

# ***SELECT***

print(select(User))

with Session(engine) as session:
    row = session.execute(select(User)).first()
    print(row)
    print(row[0])

    user = session.scalars(select(User)).first()
    print(user)


squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

print(squidward)

session = Session(engine)

session.add(squidward)
session.add(krabs)

print(session.new)
session.flush()

print(squidward)
print(krabs)

some_squidward = session.get(User, 4)
print(some_squidward)
print(some_squidward is squidward)

session.commit()

sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
print(sandy)

sandy.fullname = "Sandy Squirrel"
print(sandy in session.dirty)

sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
print(sandy_fullname)
print(sandy in session.dirty)

patrick = session.get(User, 3)

session.delete(patrick)

session.execute(select(User).where(User.name == "patrick")).first()

print(patrick in session)

session.rollback()

print(sandy.__dict__)

print(sandy.fullname)

print(sandy.__dict__)

print(patrick in session)
print(session.execute(select(User).where(User.name == "patrick")).scalar_one() is patrick)

session.close()

#print(squidward.name)

session.add(squidward)
print(squidward.name)

# ***Relationships***

u1 = User(name="pkrabs", fullname="Pearl Krabs")
print(f"addresses: {u1.addresses}")

a1 = Address(email_address="pearl.krabs@gmail.com")
u1.addresses.append(a1)
print(f"addresses: {u1.addresses}")
print(a1.user)

a2 = Address(email_address="pearl@aol.com", user=u1)
print(f"addresses: {u1.addresses}")

# equivalent effect as a2 = Address(user=u1)
a2.user = u1

session.add(u1)
print(u1 in session)
print(a1 in session)
print(a2 in session)

print(u1.id)
print(a1.user_id)

session.commit()

print(u1.id)

print(u1.addresses)

print(u1.addresses)

print(a1)

print(a2)

# ***Relationship in Queries***

print(select(Address.email_address).select_from(User).join(User.addresses))

print(select(Address.email_address).join_from(User, Address))