from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Yahoo OAuth tokens
    yahoo_access_token = Column(String, nullable=True)
    yahoo_refresh_token = Column(String, nullable=True)
    
    leagues = relationship("League", back_populates="owner")
