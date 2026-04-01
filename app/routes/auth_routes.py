from fastapi import APIRouter, HTTPException
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import UserInDb, Token
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    register_user,
)
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserInDb)
async def addUser(user: UserInDb):
    result = register_user(
        username=user.nombre,
        email=user.email,
        password=user.clave,
    )
    return result
