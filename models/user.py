from sqlalchemy import Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum as PyEnum
from db import Base
from datetime import datetime

class Role(PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email : Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    password: Mapped[str] = mapped_column(String,nullable=False)
    role : Mapped[Role] = mapped_column(Enum(Role,name="role_enum"))
    login_at : Mapped[datetime] = mapped_column(DateTime,nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now()) 
    
    