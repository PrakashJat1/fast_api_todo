from fastapi import APIRouter

todo_router = APIRouter()



@todo_router.get("/")
async def get_todo():
    return "TODO"