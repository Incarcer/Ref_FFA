from sqlalchemy import Column, Integer, String, Float, Enum as SQLAlchemyEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.db import Base
from .team import roster_association
import enum

class Position(enum.Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    K = "K"
    DEF = "DEF"

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    yahoo_player_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    position = Column(SQLAlchemyEnum(Position), nullable=False)
    nfl_team_abbr = Column(String, nullable=True)
    
    # Fields for future data enrichment
    bye_week = Column(Integer, nullable=True)
    adp = Column(Float, nullable=True)
    projection = Column(Float, nullable=True)
    
    teams = relationship(
        "Team", secondary=roster_association, back_populates="players"
    )

class PlayerValue(Base):
    __tablename__ = "player_values"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    value = Column(Integer, nullable=False)
    format = Column(String, nullable=False) # e.g., '1QB', 'Superflex'
    source = Column(String, nullable=False, default='FantasyCalc')
    date_updated = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player")

class PlayerSourceMapping(Base):
    __tablename__ = "player_source_mappings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    source_player_id = Column(String, nullable=False, index=True)
    source_player_name = Column(String, nullable=False)
    source = Column(String, nullable=False) # e.g., 'nflverse', 'fantasypros'
    
    player = relationship("Player")
