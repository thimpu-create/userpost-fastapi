from passlib.context import CryptContext
from datetime import datetime , timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
JWT_SECRET_KEY = 'JWT_SECRET_KEY'
JWT_REFRESH_SECRET_KEY = 'SECRETE_KEY'


password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_hashed_password(password : str):
    return password_context.hash(password)

def verify_password(password:str, hashed_password:str)->bool:
    return password_context.verify(password,hashed_password)

def create_access_token(subject : Union[str, Any], expires_delta : int = None ) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else :
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp" : expires_delta, "sub" : str(subject)}
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject : Union[str, Any], expires_delta : int = None ) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else :
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp" : expires_delta, "sub" : str(subject)}
    encoded_jwt = jwt.encode(to_encode,JWT_REFRESH_SECRET_KEY,ALGORITHM)
    return encoded_jwt

def decrypt_token(token : str):
    data = jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)
    username :str = data.get("sub")
    return username