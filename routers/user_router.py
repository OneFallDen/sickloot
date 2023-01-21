from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.schemas import UserReg
from controllers.user_controller import signup, signin
from sql.db import get_db


router = APIRouter()


@router.post('/reg', tags=['user'])
async def reg_new_user(user: UserReg, db: Session = Depends(get_db)):
    return signup(user, db)


@router.post('/login', tags=['user'])
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return signin(form_data, db)
