from pydantic import BaseModel, EmailStr, Field, ConfigDict,model_validator, field_validator
from models.user import Role
from fastapi.exceptions import HTTPException


class UserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True, populate_by_name=True,validate_default=True,validate_assignment=True)
    
    email : EmailStr = Field(alias="Email")
    password : str = Field(alias="Password", min_length=3,max_length=8)
    confirm_password : str = Field(alias="Confirm_Password",min_length=3,max_length=8)
    role: Role = Field(alias="Role")
    
    @field_validator("role")
    def convert_role(cls,value):
        return Role.USER if value == Role.USER.value else Role.ADMIN
    
    @model_validator(mode="after") 
    def check_password_match(self):
        if self.password != self.confirm_password:
            raise HTTPException(status_code=422,detail={
                "msg" : "Password and Confirm Password must be same"
            })
        return self

class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True,validate_default=True,validate_assignment=True,populate_by_name=True)
    
    id : int
    email : str
    role : str


class UserUpdateRequest(BaseModel):
    email: EmailStr
    
    