from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
import crud.tag_crud as crud
import schemas
from schemas import NoteUpdateResponse
from apis.dependencies import get_db
from typing import List

router = APIRouter()

# Endpoint do pobierania tagów dla konkretnej notatki użytkownika
@router.get("/tags/", response_model=List[schemas.TagRead])
def get_tags_for_note(note_id: int = Query(...),user_id: int = Query(...),api_key: str = Header(...),db: Session = Depends(get_db)):
    return crud.get_tags_for_note(db, note_id=note_id, user_id=user_id, api_key=api_key)

# Endpoint do tworzenia tagu dla konkretnej notatki użytkownika
@router.post("/tags/", response_model=schemas.TagRead, status_code=status.HTTP_201_CREATED)
def create_tag_endpoint(tag: schemas.TagCreate, user_id: int = Query(...), api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.create_tag(db, tag=tag, user_id=user_id, api_key=api_key)

# Endpoint do usunięcia tagu dla konkretnej notatki
@router.delete("/tags/{tag_id}", response_model=schemas.NoteUpdateResponse)
def delete_tag_endpoint(tag_id: int, user_id: int = Query(...), api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.delete_tag(db, tag_id=tag_id, user_id=user_id, api_key=api_key)

# Endpoint do aktualizacji tagu
@router.put("/tags/{tag_id}", response_model=schemas.NoteUpdateResponse)
def update_tag_endpoint(tag_id: int, tag_update: schemas.TagUpdate, user_id: int = Query(...), api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.update_tag(db, tag_id=tag_id, user_id=user_id, api_key=api_key, tag_update=tag_update)

