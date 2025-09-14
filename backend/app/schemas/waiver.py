from pydantic import BaseModel
from typing import List, Optional

class WaiverPlayer(BaseModel):
    player_key: str
    player_id: str
    full_name: str
    editorial_team_abbr: str
    display_position: str
    eligible_positions: List[str]
    image_url: Optional[str] = None
    percent_owned: int

    class Config:
        orm_mode = True
