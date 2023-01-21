from jose import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, PASSWORD_SALT, REFRESH_TOKEN_EXPIRE_DAYS


hasher = CryptContext(schemes=['bcrypt'])


def encode_token(username):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'sub': username
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload['scope'] == 'access_token':
            return payload['sub']
        raise HTTPException(status_code=401, detail='Scope for the token is invalid')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')


def encode_refresh_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS, minutes=0),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
        if payload['scope'] == 'refresh_token':
            user_id = payload['sub']
            new_token = encode_token(user_id)
            return new_token
        raise HTTPException(status_code=401, detail='Invalid scope for token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')


def encode_password(password):
    return hasher.hash(password + PASSWORD_SALT)


def verify_password(password, encoded_password):
    return hasher.verify(password + PASSWORD_SALT, encoded_password)
