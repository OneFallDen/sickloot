from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from models.schemas import UserReg, UserAuth
from auth.auth import encode_password, encode_token, encode_refresh_token, verify_password, decode_token
from sql.crud import check_user, add_user, get_user_id, get_encoded_password, get_user
from sql.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
security = HTTPBearer()


# Registration
def signup(user: UserReg, db: Session):
    # Check passwords match
    if user.password != user.repeat_password:
        raise 'Passwords don`t match'
    # Check is email and username unique
    msg = check_user(user.email, user.username, db)
    if msg != '':
        return msg
    try:
        # Hash password
        hashed_password = encode_password(user.password)
        # Add user in db
        add_user(user, db, hashed_password)
        # Generate and return access and refresh tokens
        access_token = encode_token(user.username)
        refresh_token = encode_refresh_token(user.username)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except:
        error_msg = 'Failed to signup user'
        return error_msg


# Login
def signin(form_data: OAuth2PasswordRequestForm, db: Session):
    try:
        # Try to find user id by username
        # Also it's checking for username: is it exists or not
        user_id = get_user_id(form_data.username, db)
    except:
        # If we don`t find user id we throw error that username is invalid
        return HTTPException(status_code=401, detail='Invalid username')
    # We get encoded password from db
    encoded_password = get_encoded_password(user_id, db)
    # Check password that user entered with hashed password in db
    if not verify_password(form_data.password, encoded_password):
        # If passwords don`t match than we throw error that password is invalid
        return HTTPException(status_code=401, detail='Invalid password')
    # If passwords match we generate and return access and refresh tokens
    access_token = encode_token(form_data.username)
    refresh_token = encode_refresh_token(form_data.username)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    user_id = get_user_id(username, db)
    user = get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=401, detail='Could not validate credentials')
    return user
