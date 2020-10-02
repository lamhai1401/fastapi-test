from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from src.models import User, User_Pydantic
from src.utils import errors
from pydantic import BaseModel
from typing import Optional
from jose import JWTError

#  to get a string like this run:
#  openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter("Oauth Router")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: str, password_hash: str):
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    print(user.dict())
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def get_user(username: str):
    return await User_Pydantic.from_queryset_single(User.get(username=username))


async def verify_token(token: str):
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return "Username {} is invalid".format(username)
        user = await get_user(username)
        if user is None:
            raise await errors.Error404("Username {} is invalid".format(username))
    except JWTError as jw:
        raise await errors.Error401(str(jw))
    except Exception as ex:
        raise await errors.Error404(str(ex))
