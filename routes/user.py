from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from fastapi.exceptions import HTTPException
from db import get_db
from models.user import User, Role
from schemas.user import UserResponse, UserUpdateRequest
from utils import get_current_user,authorize, is_current_user


user_router = APIRouter()

@user_router.get("/")
async def get_users(current_user : User = Depends(authorize(allowed_roles=[Role.ADMIN.value])),db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User.id,User.email,User.role,User.created_at, User.login_at))
    return result.mappings().all()

@user_router.get("/{id}",response_model=UserResponse)
async def get_user_by_id(id : int,current_user : User = Depends(authorize(allowed_roles=[Role.ADMIN.value])), db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    return result.scalars().first()

@user_router.put("/{id}",response_model=UserResponse)
async def update_user(id: int,updated_user : UserUpdateRequest, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(User).where(User.id == id))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail= f"User with id '{id}' not exist")
    
    is_current_user(existing_user)
    if updated_user.email is not None:
        result = await db.execute(select(User).where(and_(User.email == updated_user.email, User.id != id)))
        if result.scalar_one_or_none() is not None:
            raise HTTPException(status_code=400,detail=f"User with '{updated_user.email}' already exist")
    
    result = await db.execute(update(User).where(User.id == id).values(**updated_user.model_dump()).returning(User))
    await db.commit()
    return result.scalars().first()
    
@user_router.delete("/{id}")
async def delete_user(id : int,current_user = Depends(authorize(allowed_roles = [Role.ADMIN.value])), db : AsyncSession = Depends(get_db)):
    result = await db.execute(delete(User).where(User.id == id))
    await db.commit()
    if result.rowcount == 0: # type: ignore
        raise HTTPException(status_code=404, detail=f"User not found with id '{id}'")
    return JSONResponse(status_code=200,content={"msg" : "user deleted successfully"})
            
    pass