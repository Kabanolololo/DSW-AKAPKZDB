from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Model użytkownika
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    # Relacja do notatek
    notes = relationship("Note", back_populates="owner")
