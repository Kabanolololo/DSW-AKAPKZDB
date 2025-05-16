from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schematy tagi
class TagCreate(BaseModel):
    name: str
    note_id: int

class TagRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    note_id: int

    class Config:
        orm_mode = True
        
class TagUpdate(BaseModel):
    name: Optional[str] = None
    note_id: Optional[int] = None
    updated_at: datetime