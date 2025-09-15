from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base
# Import YahooToken to ensure SQLAlchemy recognizes the relationship
from app.models.yahoo_token import YahooToken

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    # Relationship to YahooToken (one-to-one)
    yahoo_token = relationship(
        "YahooToken",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )