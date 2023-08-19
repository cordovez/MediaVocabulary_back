
from typing import Annotated
from datetime import datetime, timedelta


from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user_models import User, User_Register, User_MongoDB

from ..authorization.auth import get_current_active_user, Token, authenticate_user, create_access_token, get_password_hash # noqa: E501


users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "e43ebd3d25e44ab359405c8a53992e92141d012466c8c760d3c3bf40cc961e8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@users_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated
                                 [OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user( form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password", 
                            headers={"WWW-Authenticate": "Bearer"},)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@users_router.post("/users/register")
async def add_user(user_input: User_Register):
    hash = get_password_hash(user_input.password)
    new_user =  User_MongoDB(username = user_input.username, 
                             email= user_input.email, hashed_password= hash)
    await new_user.create()
    
    return new_user



