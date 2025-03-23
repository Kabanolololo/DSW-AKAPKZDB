from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserLogin
from models import User
from models import ApiKey
from apis.dependencies import get_db
from authorization.auth import hash_password_sha256,generate_api_key

router = APIRouter()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Sprawdzamy, czy użytkownik istnieje w bazie danych
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Jeżeli użytkownik nie istnieje lub hasło jest niepoprawne
    if not db_user or not hash_password_sha256(user.password) == db_user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Pobieramy klucz API użytkownika
    api_key = db.query(ApiKey).filter(ApiKey.user_id == db_user.id).first()
    
    # Jeśli nie znaleziono klucza API, zgłaszamy błąd
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key not found"
        )

    # Zwracamy API Key
    return {"api_key": api_key.key}

@router.post("/logout")
def logout(api_key: str, db: Session = Depends(get_db)):
    # Sprawdzamy, czy klucz API jest powiązany z użytkownikiem
    db_api_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    # Usuwamy stary klucz API
    db.delete(db_api_key)
    db.commit()
    
    # Generujemy nowy klucz API
    new_api_key = generate_api_key()
    new_api_key_record = ApiKey(key=new_api_key, user_id=db_api_key.user_id)
    db.add(new_api_key_record)
    db.commit()

    return {"new_api_key": new_api_key}
