from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from schemas import UserCreate

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

# Funkcja do pobierania użytkowników
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Funkcja do pobierania użytkownika po ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Funkcja do pobierania użytkownika po emailu
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
