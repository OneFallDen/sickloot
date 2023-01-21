from sqlalchemy import select
from sqlalchemy.orm import Session

from sql import models
from models import schemas


"""
    USER
"""


def check_user(email: str, login: str, db: Session):
    result = db.execute(select(models.User).where(models.User.email == email)).first()
    if result:
        return 'User with that email already exists'
    result = db.execute(select(models.User).where(models.User.login == login)).first()
    if result:
        return 'User with that username already exists'
    return ''


def add_user(user: schemas.UserReg, db: Session, hashed_password: str):
    db_user = models.User(
        login=user.login,
        password=hashed_password,
        email=user.email,
        opened_cases=0,
        level=1,
        steam_acc_url='',
        role=0,
        balance=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_id(login: str, db: Session):
    result = db.execute(select(models.User).where(models.User.login == login)).first()
    return result[0].id


def get_encoded_password(user_id: int, db: Session):
    result = db.execute(select(models.User).where(models.User.id == user_id)).first()
    return result[0].password


def get_user(user_id: int, db: Session):
    result = db.execute(select(models.User).where(models.User.id == user_id)).first()
    return result[0]
