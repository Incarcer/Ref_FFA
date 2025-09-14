from pydantic import BaseModel
from typing import List

class TradeRequest(BaseModel):
    my_player_ids: List[int]
    their_player_ids: List[int]
    league_format: str = "Superflex"

class PlayerTradeInfo(BaseModel):
    player_id: int
    name: str
    position: str
    value: int

class TradeSideAnalysis(BaseModel):
    players: List[PlayerTradeInfo]
    total_value: int

class TradeAnalysis(BaseModel):
    my_side: TradeSideAnalysis
    their_side: TradeSideAnalysis
    recommendation: str
    value_difference: int

    class Config:
        from_attributes = True
