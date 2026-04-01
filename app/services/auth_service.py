from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from app.schemas.schemas import User, UserInDb, TokenData
from app.services.user_service import UserService
from config import ALGORITHM, SECRET_KEY, HASH_DUMMY


password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash(HASH_DUMMY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
user_service = UserService()


def hashed_password(plain_password):
    return password_hash.hash(password=plain_password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)


def authenticate_user(email: str, password: str):
    user = user_service.existing_user(email=email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.clave):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        print(email)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = user_service.existing_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.estado == "inactivo":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def register_user(username, email, password):
    hash_password = hashed_password(password)
    return user_service.create_user(
        username=username, email=email, password=hash_password
    )
