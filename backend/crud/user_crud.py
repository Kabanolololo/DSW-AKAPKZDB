from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from models import ApiKey
from crud.auth_crud import get_user_by_api_key
from schemas import UserCreate, UserUpdate
from authorization.auth import hash_password_sha256

# Funkcja do tworzenia użytkownika
def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    # Sprawdzamy, czy użytkownik z takim emailem już istnieje
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Haszowanie hasła
    hashed_password = hash_password_sha256(user.password)
    db_user = User(email=user.email, password=hashed_password)
    
    try:
        # Dodajemy użytkownika do bazy
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Zwracamy komunikat o powodzeniu (BEZ tworzenia API Key)
        return {"message": "Successfully created a user. Go to the login page and log in to your new account."}
    
    except Exception as e:
        db.rollback()  # Jeśli coś pójdzie nie tak, cofnij zmiany
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        ) from e

# Funkcja do wyświetlania konkretnego użytkownika        
def get_user(db: Session, user_id: int, api_key: str) -> User:
    # Weryfikujemy API Key i otrzymujemy użytkownika
    user = get_user_by_api_key(db, api_key)

    # Sprawdzamy, czy API Key jest powiązany z tym użytkownikiem
    if user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this user"
        )
    
    return user

# Funkcja do aktualizacji użytkownika
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_fields = []  # Lista do przechowywania zaktualizowanych pól

    if user_update.email:
        user.email = user_update.email
        updated_fields.append("email")
    if user_update.password:
        user.password = hash_password_sha256(user_update.password)
        updated_fields.append("password")

    if updated_fields:
        db.commit()
        db.refresh(user)
        
        message = "Updated: "
        message += ", ".join(updated_fields)
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail="No data provided for update")