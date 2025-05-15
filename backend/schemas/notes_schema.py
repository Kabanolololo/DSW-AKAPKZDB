from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
