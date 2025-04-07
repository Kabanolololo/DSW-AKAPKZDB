from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.tag_model import Tag
from models.note_model import Note
from schemas import TagCreate, TagRead, TagUpdate, NoteUpdateResponse
from crud.auth_crud import check_api_key_permissions

# Funkcja do wyświetlenia tagów dla konkretnej notatki użytkownika
def get_tags_for_note(db: Session, note_id: int, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    tags = db.query(Tag).filter(Tag.note_id == note_id).all()
    if not tags:
        raise HTTPException(status_code=404, detail="No tags found for this note")
    
    return tags

# Funkcja do stworzenia tagu dla notatki konkretnego uzytkownika
def create_tag(db: Session, tag: TagCreate, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Tworzymy nową notatkę
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    return db_tag

# Funkcja do aktualizacji tagu
def update_tag(db: Session, tag_id: int, user_id: int, api_key: str, tag_update: TagUpdate):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    note = db.query(Note).filter(Note.id == tag.note_id).first()
    if not note or note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this tag or note")
    if tag_update.name:
        tag.name = tag_update.name
    
    db.commit()
    db.refresh(tag)

    return {"message": "Tag updated successfully"}

# Funkcja do usunięcia tagu (bez potrzeby podawania note_id)
def delete_tag(db: Session, tag_id: int, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    note = db.query(Note).filter(Note.id == tag.note_id).first()
    if not note or note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this tag or note")
    
    db.delete(tag)
    db.commit()
    
    return {"message": "Tag deleted successfully"}