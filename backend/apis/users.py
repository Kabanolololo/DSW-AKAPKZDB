from fastapi import APIRouter, Depends, HTTPException, status, Query,Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import crud.user_crud as crud
import schemas
from schemas import UpdateResponse, CreateResponse
from apis.dependencies import get_db

router = APIRouter()

# Endpoint do tworzenia użytkownika
@router.post("/users/", response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Wywołanie funkcji do tworzenia użytkownika z `crud.py`
        return crud.create_user(db=db, user=user)
    except HTTPException as e:
        raise e

# Endpoint do wyświetlania szczegółów użytkownika
@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, api_key: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id, api_key=api_key)
    return user

# Endpoint do wyświetlania nicku
@router.get("/users/{user_id}/nick")
def read_user_nick(user_id: int, api_key: str, db: Session = Depends(get_db)):
    # Wywołanie funkcji z CRUD, aby pobrać nick użytkownika
    user_nick = crud.get_user_nick(db=db, user_id=user_id, api_key=api_key)
    if not user_nick:
        raise HTTPException(status_code=404, detail="Nick not found")
    return {"nick": user_nick}

# Endpoint do aktualizacji użytkownika
@router.put("/users/{user_id}", response_model=UpdateResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, api_key: str, db: Session = Depends(get_db)):
    try:
        # Wywołanie funkcji do aktualizacji użytkownika z `crud.py`
        return crud.update_user(db=db, user_id=user_id, api_key=api_key, user_update=user_update)
    except HTTPException as e:
        raise e