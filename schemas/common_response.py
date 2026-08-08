from schemas.user import UserResponse
from schemas.todo import SimpleTodoResponse

class TodoWithUserResponse(SimpleTodoResponse):
    user : UserResponse | None = None

class UserWithTodosResponse(UserResponse):
    todos : list["SimpleTodoResponse"] | None = None