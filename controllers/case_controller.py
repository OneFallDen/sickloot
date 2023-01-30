from sqlalchemy.orm import Session
from fastapi import HTTPException
import random as rnd

from sql.crud import get_case_by_id, get_case_items, update_balance, add_item_in_inv, add_item_in_drop_history, \
    get_item_by_id, count_cases
from models.schemas import User


def get_case(case_id: int, db: Session):
    return get_case_by_id(case_id, db)


def get_case_with_items(case_id: int, db: Session):
    case = get_case_by_id(case_id, db)
    items = get_case_items(case_id, db)
    return {
        'item': items
    }


def opened_case(case_id: int, user: User, db: Session):
    case = get_case_by_id(case_id, db)
    if user.balance < case.price:
        raise HTTPException(status_code=400, detail='Not enough money on balance')
    delta_balance = case.price * (-1)
    update_balance(delta_balance, user.id, db)
    items = get_case_items(case_id, db)
    item_num = rnd.randint(0, len(items) - 1)
    item = items[item_num]
    item_id = item.id
    add_item_in_inv(item_id, user.id, db)
    add_item_in_drop_history(user.id, case_id, item_id, db)
    count_cases(user.id, db)
    return get_item_by_id(item_num+1, db)
