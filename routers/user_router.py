from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.schemas import Token, UserReg
from controllers.user_controller import signup
from sql.db import get_db


router = APIRouter()


@router.post('/reg', tags=['user'])
async def reg_new_user(user: UserReg, db: Session = Depends(get_db)):
    return signup(user, db)
