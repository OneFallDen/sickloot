from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.schemas import User
from controllers.user_controller import get_current_user
from controllers.balance_controller import balance_rep, balance_wind
from sql.db import get_db


router = APIRouter()


@router.post('/balance/rep', tags=['balance'])
async def replenish_balance(rep_balance: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return balance_rep(rep_balance, user.id, db)


@router.post('/balance/wind', tags=['balance'])
async def windrow_balance(win_balance: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return balance_wind(win_balance, user.id, db)
