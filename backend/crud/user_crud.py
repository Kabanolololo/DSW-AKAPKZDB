from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate
from authorization.auth import hash_password_sha256
from crud.auth_crud import check_api_key_permissions

# Funkcja do tworzenia użytkownika
def create_user(db: Session, user: UserCreate):
    # Sprawdzamy, czy użytkownik z takim emailem już istnieje
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Haszowanie hasła
    hashed_password = hash_password_sha256(user.password)
    
    # Tworzenie nowego użytkownika
    db_user = User(email=user.email, password=hashed_password, nick=user.nick)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Zwracamy komunikat
        return {"message": "Successfully created a user. Go to the login page and log in to your new account."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        ) from e

# Funkcja do wyświetlania danych bieżącego użytkownika
def get_user(db: Session, user_id: int, api_key: str) -> User:
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Pobieramy użytkownika
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

# Funkcja do aktualizacji użytkownika
def update_user(db: Session, user_id: int, api_key: str, user_update: UserUpdate):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Pobieramy użytkownika do aktualizacji
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_fields = []

    # Sprawdzamy i aktualizujemy email
    if user_update.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        db_user.email = user_update.email
        updated_fields.append("email")

    # Sprawdzamy i aktualizujemy hasła
    if user_update.password:
        db_user.password = hash_password_sha256(user_update.password)
        updated_fields.append("password")
        
    # Sprawdzamy i aktualizujemy nick
    if user_update.nick:
        db_user.nick = user_update.nick
        updated_fields.append("nick")

    if updated_fields:
        db.commit()
        db.refresh(db_user)

        message = "Updated: "
        message += ", ".join(updated_fields)
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail="No data provided for update")

# Funkcja do wyświetlenia nicku użytkownika
def get_user_nick(db: Session, user_id: int, api_key: str):
    # Sprawdzamy uprawnienia użytkownika za pomocą API Key
    check_api_key_permissions(db, api_key, user_id)
    
    # Pobieramy dane użytkownika:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.nick
