from fastapi import APIRouter, Depends
from utils import get_current_user, authorize
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models.todo import TODO
from schemas.todo import TodoCreate,TodoResponse,TodoUpdate 
from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from models.user import User, Role

todo_router = APIRouter()


@todo_router.post("/create", response_model=TodoResponse)
async def create_todo(todo : TodoCreate,current_user : User = Depends(authorize([Role.USER])), db : AsyncSession = Depends(get_db)):
    todo_data = TODO(**todo.model_dump())
    todo_data.user_id = current_user.id
    db.add(todo_data)
    await db.commit()
    await db.refresh(todo_data)
    return todo_data

@todo_router.get("/get_my_todos",response_model=list[TodoResponse])
async def get_todo(current_user : User = Depends(authorize([Role.USER])), db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(TODO).where(TODO.user_id == current_user.id).order_by(TODO.id))
    return result.scalars().all()
    
@todo_router.patch("/{todo_id}",response_model=TodoResponse)
async def update_todo(todo_id : int,updated_todo : TodoUpdate ,current_user : User = Depends(authorize([Role.USER])),db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(TODO).where(TODO.id == todo_id))
    existing_todo = result.scalar_one_or_none()
    if existing_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Todo not exist with id '{todo_id}")
    
    result = await db.execute(update(TODO).where(TODO.id == todo_id).values(**updated_todo.model_dump(exclude_unset=True)).returning(TODO))
    await db.commit()
    return result.scalars().first()


    
    
    