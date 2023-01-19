import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


from sql.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user_entity"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    opened_cases = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    steam_acc_url = Column(String(255))
    role = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)


def create_db_and_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    if sys.argv[1] == 'createdb':
        create_db_and_tables()
    elif sys.argv[1] == 'dropdb':
        drop_tables()
