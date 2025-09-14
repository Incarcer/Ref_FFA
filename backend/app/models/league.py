from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from ..core.db import Base
import enum

class ScoringType(enum.Enum):
    PPR = "PPR"
    HALF_PPR = "Half-PPR"
    STANDARD = "Standard"

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    yahoo_league_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    season = Column(Integer, nullable=False)
    scoring_type = Column(SQLAlchemyEnum(ScoringType), nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="leagues")
    
    teams = relationship("Team", back_populates="league")
