from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# Schematy użytkownika
class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    nick: str
    password: constr(min_length=8)
    
class CreateResponse(BaseModel):
    message: str
    
class User(UserBase):
    id: int
    nick: str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nick: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    
    class Config:
        orm_mode = True

class UpdateResponse(BaseModel):
    message: str
    
class UserDelete(BaseModel):
    user_id: int
