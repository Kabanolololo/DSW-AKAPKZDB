from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from schemas import UserCreate
from models import Note
from schemas import NoteCreate,NoteUpdate

# Funkcja do tworzenia nowego użytkownika
def create_user(db: Session, user: UserCreate):
    # Sprawdzamy, czy użytkownik z takim emailem już istnieje
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Tworzymy nowego użytkownika
    db_user = User(**user.dict())  # używamy .dict() zamiast .model_dump()

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        ) from e

# Funkcja do wyśweitalnia konkretnego użytkownika        
def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# Funkcja do aktualizacji użytkownika
def update_user(db: Session, user_id: int, user_update: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Aktualizacja danych użytkownika
    user.email = user_update.email
    user.password = user_update.password

    db.commit()
    db.refresh(user)
    return user

# Funkcja do wyświetlania wszystkich notatek dla konkretnego użytkownika
def get_notes(db: Session, user_id: int):
     return db.query(Note).filter(Note.user_id == user_id).all()
 
 # Funkcja do pobrania szczegółów notatki dla jednego użytkownika
def get_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or does not belong to this user")
    return note

# Funkcja do stworzenia notatki
def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Funkcja do zupdetowania notatki
def update_note(db: Session, note_id: int, user_id: int, note_update: NoteUpdate):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Sprawdzamy, czy notatka należy do użytkownika
    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    # Aktualizacja tytulu i treści notatki
    note.title = note_update.title
    note.content = note_update.content
    db.commit()
    db.refresh(note)
    return note

# Funkcja do usunięcia notatki
def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Sprawdzamy, czy notatka należy do użytkownika
    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this note")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
