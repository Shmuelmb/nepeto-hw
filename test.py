from sqlalchemy import (
    Column, DateTime, Float, ForeignKey, Integer, JSON, String, func
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))


engine = create_engine(
    'postgresql://root:1234@localhost:5432/users', echo=True)
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)

session = Session()
session.add(User(name='wendy', fullname='Wendy Williams', nickname='windy'))
session.commit()
