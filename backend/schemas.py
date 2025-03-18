from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# Bazowy schemat użytkownika (część wspólna)
class UserBase(BaseModel):
    email: EmailStr

# Schemat do tworzenia nowego użytkownika
class UserCreate(UserBase):
    password: constr(min_length=8)  # Minimalna długość hasła, np. 8 znaków

# Schemat użytkownika z ID (do zwrócenia po utworzeniu użytkownika)
class User(UserBase):
    id: int

    # Ustawiamy orm_mode = True, aby Pydantic mogło poprawnie serializować dane z SQLAlchemy
    class Config:
        orm_mode = True

# Schemat odpowiedzi błędu
class ErrorResponse(BaseModel):
    detail: str
