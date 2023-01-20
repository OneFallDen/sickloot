from jose import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, PASSWORD_SALT, REFRESH_TOKEN_EXPIRE_DAYS


class Auth():
    hasher = CryptContext(schemes=['bcrypt'])

    def encode_password(self, password):
        return self.hasher.hash(password, secret=PASSWORD_SALT)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password, secret=PASSWORD_SALT)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if payload['scope'] == 'accsess_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')

    def encode_refresh_token(self, user_id):
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

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
            if payload['scope'] == 'refresh_token':
                user_id = payload['sub']
                new_token = self.encode_token(user_id)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
