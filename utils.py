import enum
from jose import jwt
from jose.exceptions import JWTError
import os
from models.user import User, Role
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.exceptions import HTTPException
from db import get_db
from fastapi import Depends, status
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

load_dotenv()

get_token = OAuth2PasswordBearer(tokenUrl="/api/auth/login",scheme_name="JWT")

JWT_ACCESS_TOKEN_SECRET = os.getenv("JWT_ACCESS_TOKEN_SECRET","my-access-secret")
JWT_REFRESH_TOKEN_SECRET = os.getenv("JWT_REFRESH_TOKEN_SECRET","my-refresh-secret")
JWT_ALGO = os.getenv("JWT_ALGO","HS256")
JWT_ACESS_TOKEN_EXPIRE = os.getenv("JWT_ACESS_TOKEN_EXPIRE",30)
JWT_REFRESH_TOKEN_EXPIRE = os.getenv("JWT_REFRESH_TOKEN_EXPIRE",60*24*7)


def get_hashed_password(password : str) -> str:
    return password_context.hash(password)

def verify_password(raw_password : str,hashed_password : str) -> bool:
    is_verified = password_context.verify(raw_password,hashed_password)
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Wrong Password")
    else:
        return True

def create_token(user : User,type="access") -> str:
    jwt_exp = JWT_ACESS_TOKEN_EXPIRE if type == "access" else JWT_REFRESH_TOKEN_EXPIRE
    expiry = datetime.now(timezone.utc) + timedelta(minutes=int(jwt_exp))
    payload = {
        "user_id" : user.id,
        "user_role" : user.role.value,
        "exp" : expiry,
        "type": type
    }
    JWT_SECRET = JWT_ACCESS_TOKEN_SECRET if type == "access" else JWT_REFRESH_TOKEN_SECRET
    token : str = jwt.encode(payload,JWT_SECRET,JWT_ALGO)
    return token

def verify_token(token : str,type="access") -> dict:
    JWT_SECRET = JWT_ACCESS_TOKEN_SECRET if type == "access" else JWT_REFRESH_TOKEN_SECRET
    try:
        payload = jwt.decode(token,JWT_SECRET,JWT_ALGO)
    except JWTError as e:
        raise HTTPException(status_code=400,detail=e)
    
    if payload["exp"] < datetime.now().timestamp():
        raise HTTPException(status_code=400,detail={
            "msg" : "Token Expired"
        })
    return payload

#Current user without authorize check
async def get_current_user(token : str = Depends(get_token),db : AsyncSession = Depends(get_db)) -> User:
    
    payload = verify_token(token)
    user_id = payload["user_id"]
    user_role = Role(payload["user_role"])              
    result = await db.execute(select(User).where(User.id == user_id,User.role == user_role))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={
            "msg" : "User not matched"
        })
    return user

#Current user + authorize check
def authorize(allowed_roles : list[str]):
    async def checker(user : User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You don't have permission to access this endpoint")
        else:
            return user
    
    return checker
        
def is_current_user(incoming_user: User, current_user : User):
    if incoming_user.id != current_user.id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not an authorized person to acess this operation")
    