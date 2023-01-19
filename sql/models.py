import sys
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from sql.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    opened_cases = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    steam_acc_url = Column(String(255))
    role = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)

    windrows = relationship('Windrow_History', backref='user')
    inventory = relationship('Inventory', backref='user')
    drop_user = relationship('DropHistory', backref='user')


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    character = Column(String(255), nullable=False)
    rarity = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    inventory = relationship('Inventory', backref='item')
    drop_item = relationship('DropHistory', backref='item')


class Case(Base):
    __tablename__ = 'case'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    case_items = relationship('CaseItems', backref='case')
    drop_case = relationship('DropHistory', backref='case')


class Sett(Base):
    __tablename__ = 'set'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    character = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    set_items = relationship('SetItems', backref='set')


class Windrow_History(Base):
    __tablename__ = 'windrow_history'

    user_id = Column(Integer, ForeignKey('user.id'))
    win_rep = Column(Integer, nullable=False)
    date = Column(DateTime,  default=datetime.utcnow())


class Inventory(Base):
    __tablename__ = 'inventory'

    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('item.id'))


class CaseItems(Base):
    __tablename__ = 'case_items'

    case_id = Column(Integer, ForeignKey('case.id'))
    item_id = Column(Integer, ForeignKey('item.id'))


class SetItems(Base):
    __tablename__ = 'set_items'

    set_id = Column(Integer, ForeignKey('set.id'))
    item_id = Column(Integer, ForeignKey('item.id'))


class DropHistory(Base):
    __tablename__ = 'drop_history'

    user_id = Column(Integer, ForeignKey('user.id'))
    case_id = Column(Integer, ForeignKey('case.id'))
    item_id = Column(Integer, ForeignKey('item.id'))


def create_db_and_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    if sys.argv[1] == 'createdb':
        create_db_and_tables()
    elif sys.argv[1] == 'dropdb':
        drop_tables()
