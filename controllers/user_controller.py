from fastapi.security import HTTPBearer
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.schemas import UserReg, UserAuth
from auth.auth import encode_password, encode_token, encode_refresh_token, verify_password
from sql.crud import check_user, add_user, get_user_id, get_encoded_password


security = HTTPBearer()


def signup(user: UserReg, db: Session):
    if user.password != user.repeat_password:
        raise 'Passwords don`t match'
    msg = check_user(user.email, user.login, db)
    if msg != '':
        return msg
    try:
        hashed_password = encode_password(user.password)
        add_user(user, db, hashed_password)
        user_id = get_user_id(user.login, db)
        access_token = encode_token(user_id)
        refresh_token = encode_refresh_token(user_id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except:
        error_msg = 'Failed to signup user'
        return error_msg


def signin(user: UserAuth, db: Session):
    try:
        user_id = get_user_id(user.login, db)
    except:
        return HTTPException(status_code=401, detail='Invalid username')
    encoded_password = get_encoded_password(user_id, db)
    if not verify_password(user.password, encoded_password):
        return HTTPException(status_code=401, detail='Invalid password')
    access_token = encode_token(user_id)
    refresh_token = encode_refresh_token(user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
