from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

# Schematy użytkownika
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LogoutRequest(BaseModel):
    api_key: str
    
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)
    
class CreateResponse(BaseModel):
    message: str

class User(UserBase):
    id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    
    class Config:
        orm_mode = True

class UpdateResponse(BaseModel):
    message: str

# Schematy notatek
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteUpdateResponse(BaseModel):
    message: str


class Note(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True