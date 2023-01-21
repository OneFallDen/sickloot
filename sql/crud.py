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
        login=user.username,
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


"""
    BALANCE
"""


def update_balance(delta_balance: int, user_id: int, db: Session):
    result = db.execute(select(models.User).where(models.User.id == user_id)).first()
    balance = result[0].balance
    new_balance = balance + delta_balance
    if new_balance < 0:
        return False
    db.query(models.User).filter(models.User.id == user_id).update(
        {
            models.User.balance: new_balance
        }
    )
    db.commit()
    return True


"""
    CASE
"""


def get_case_by_id(case_id: int, db: Session):
    result = db.execute(select(models.Case).where(models.Case.id == case_id)).first()
    return result[0]


def get_case_items(case_id: int, db: Session):
    result = db.execute(select(models.CaseItems).where(models.CaseItems.case_id == case_id))
    items = []
    items_res = result.scalars().all()
    for res in items_res:
        res_items = db.execute(select(models.Item).where(models.Item.id == res.item_id)).first()
        items.append(res_items[0])
    return items
