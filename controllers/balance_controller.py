from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import update_balance


def balance_rep(rep_balance: int, user_id: int, db: Session):
    if not rep_balance > 0:
        raise HTTPException(status_code=400, detail='Invalid sum for replenishment')
    update_balance(rep_balance, user_id, db)
    return HTTPException(status_code=201, detail='Balance replenished successfully')


def balance_wind(win_balance: int, user_id: int, db: Session):
    if win_balance == 0:
        raise HTTPException(status_code=400, detail='Invalid sum for windrow')
    if win_balance > 0:
        win_balance = win_balance * (-1)
    if update_balance(win_balance, user_id, db):
        return HTTPException(status_code=201, detail='Balance windrow successfully')
    else:
        return HTTPException(status_code=400, detail='Invalid sum for windrow')

