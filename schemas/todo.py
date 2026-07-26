from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from schemas.user import UserResponse

class TodoCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True,from_attributes=True,validate_assignment=True,validate_default=True,validate_by_alias=True)
    
    title : str
    description : str

class TodoResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True,from_attributes=True)
    
    id : int
    user : UserResponse
    title : str
    description : str
    is_completed : bool
    created_at : datetime

class TodoUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True,from_attributes=True,validate_assignment=True,validate_default=True,validate_by_alias=True)
    
    title : str|None = None
    description : str|None = None
    is_completed : bool|None = None
