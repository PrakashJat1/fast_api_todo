from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

# class TODO(Base):
#     __table__ = "todo" # type: ignore
    
#     id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),back_populates="user")
#     user: Mapped["User"] = relationship(back_populates="user") #  type: ignore
#     title : Mapped[str] = mapped_column(String,nullable=False,unique=True)
#     description : Mapped[str] = mapped_column(String, nullable= True)
#     is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now())
    