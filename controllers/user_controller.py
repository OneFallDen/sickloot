from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from models.schemas import UserReg
from auth.auth import encode_password, encode_token, encode_refresh_token
from sql.crud import check_user, add_user, get_user_id


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
