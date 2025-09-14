from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..core.db import Base

# Association table for the many-to-many relationship between teams and players
roster_association = Table(
    "roster_association",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    yahoo_team_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    
    league_id = Column(Integer, ForeignKey("leagues.id"))
    league = relationship("League", back_populates="teams")

    players = relationship(
        "Player", secondary=roster_association, back_populates="teams"
    )
