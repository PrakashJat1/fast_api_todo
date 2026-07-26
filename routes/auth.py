from fastapi import APIRouter
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from fastapi.exceptions import HTTPException
from db import get_db
from models.user import User
from schemas.auth import UserRegister, UserLogin
from utils import get_hashed_password, verify_password, create_token

auth_router = APIRouter()
#Hyy

@auth_router.post('/register')
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400,detail={
            "msg" : f"Email already exist ''"
        })
        
    hashed_password = get_hashed_password(password=user.password)
    user_data = User(email=user.email,password=hashed_password,role=user.role)
    
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data

@auth_router.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" User not exist with email '{user.email}")
    
    verify_password(user.password,existing_user.password)
    access_token = create_token(existing_user)
    refresh_token = create_token(existing_user,type="refresh")
    
    return JSONResponse(status_code=status.HTTP_200_OK,content={
        "access_token" : access_token,
        "refresh_token" : refresh_token
    })