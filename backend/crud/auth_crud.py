from sqlalchemy.orm import Session
from models import ApiKey, User
from fastapi import HTTPException, status

# Funkcja do weryfikowania klucza API
def verify_api_key(db: Session, api_key: str) -> ApiKey:
    # Sprawdzamy, czy klucz API jest prawidłowy
    db_api_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    return db_api_key

# Funckja do wyświetlania szczegółów użytkownika
def get_user_by_api_key(db: Session, api_key: str) -> User:
    # Weryfikujemy klucz API
    db_api_key = verify_api_key(db, api_key)
    
    # Pobieramy użytkownika powiązanego z tym API Key
    user = db.query(User).filter(User.id == db_api_key.user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
