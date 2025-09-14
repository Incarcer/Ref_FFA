from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..models.player import Player, PlayerValue
from ..schemas.trade import TradeRequest, TradeAnalysis, TradeSideAnalysis, PlayerTradeInfo

def get_player_values(db: Session, player_ids: List[int], league_format: str) -> List[PlayerTradeInfo]:
    if not player_ids:
        return []
    
    subquery = db.query(
        PlayerValue.player_id,
        func.max(PlayerValue.date_updated).label('max_date')
    ).filter(
        PlayerValue.player_id.in_(player_ids),
        PlayerValue.format == league_format
    ).group_by(PlayerValue.player_id).subquery()

    results = db.query(
        Player.id,
        Player.name,
        Player.position,
        PlayerValue.value
    ).join(
        PlayerValue, Player.id == PlayerValue.player_id
    ).join(
        subquery,
        (PlayerValue.player_id == subquery.c.player_id) &
        (PlayerValue.date_updated == subquery.c.max_date)
    ).filter(
        PlayerValue.format == league_format
    ).all()
    
    return [
        PlayerTradeInfo(player_id=r.id, name=r.name, position=r.position.value, value=r.value)
        for r in results
    ]

def analyze_trade(db: Session, trade_request: TradeRequest) -> TradeAnalysis:
    my_players_info = get_player_values(db, trade_request.my_player_ids, trade_request.league_format)
    their_players_info = get_player_values(db, trade_request.their_player_ids, trade_request.league_format)

    my_total_value = sum(p.value for p in my_players_info)
    their_total_value = sum(p.value for p in their_players_info)

    value_difference = my_total_value - their_total_value
    
    if my_total_value == 0 and their_total_value == 0:
        recommendation = "Cannot analyze a trade with players of zero value."
    elif my_total_value == 0 and their_total_value > 0:
        recommendation = "You are receiving value for nothing. Accept this trade."
    elif their_total_value == 0 and my_total_value > 0:
        recommendation = "You are giving away value for nothing. Decline this trade."
    else:
        average_trade_value = (my_total_value + their_total_value) / 2
        percentage_diff = (value_difference / average_trade_value) * 100

        if percentage_diff > 10:
            recommendation = "This trade is heavily in your favor. It's a clear accept."
        elif percentage_diff > 3:
            recommendation = "This trade looks favorable for you. Recommended to accept."
        elif percentage_diff < -10:
            recommendation = "This trade is heavily against you. It's a clear decline."
        elif percentage_diff < -3:
            recommendation = "This trade is not in your favor. Recommended to decline or renegotiate."
        else:
            recommendation = "This trade appears to be fairly balanced."

    my_side = TradeSideAnalysis(players=my_players_info, total_value=my_total_value)
    their_side = TradeSideAnalysis(players=their_players_info, total_value=their_total_value)

    return TradeAnalysis(
        my_side=my_side,
        their_side=their_side,
        recommendation=recommendation,
        value_difference=value_difference
    )
