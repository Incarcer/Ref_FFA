from typing import List
import xml.etree.ElementTree as ET
from backend.app.services import yahoo_api
from backend.app.schemas.waiver import WaiverPlayer

# The namespace is required to parse Yahoo's XML response correctly.
YAHOO_NAMESPACE = {'y': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng'}

def _parse_player_element(player_element: ET.Element) -> WaiverPlayer:
    """
    Parses a single player XML element and returns a WaiverPlayer schema object.
    """
    def find_text(tag: str) -> str:
        element = player_element.find(f'y:{tag}', YAHOO_NAMESPACE)
        return element.text if element is not None else ''

    def find_nested_text(parent_tag: str, child_tag: str) -> str:
        parent = player_element.find(f'y:{parent_tag}', YAHOO_NAMESPACE)
        if parent is not None:
            child = parent.find(f'y:{child_tag}', YAHOO_NAMESPACE)
            return child.text if child is not None else ''
        return ''

    eligible_positions = [
        pos.text for pos in player_element.findall('.//y:eligible_positions/y:position', YAHOO_NAMESPACE)
        if pos.text is not None
    ]
    
    percent_owned_text = find_nested_text('percent_owned', 'value')

    return WaiverPlayer(
        player_key=find_text('player_key'),
        player_id=find_text('player_id'),
        full_name=find_nested_text('name', 'full'),
        editorial_team_abbr=find_text('editorial_team_abbr'),
        display_position=find_text('display_position'),
        eligible_positions=eligible_positions,
        image_url=find_nested_text('headshot', 'url'),
        percent_owned=int(percent_owned_text) if percent_owned_text else 0
    )

def process_waiver_data(access_token: str, league_key: str) -> List[WaiverPlayer]:
    """
    Fetches waiver wire players from the Yahoo API and transforms the data
    into a list of WaiverPlayer objects.
    """
    # 1. Call the yahoo_api service to get raw player data
    raw_player_elements = yahoo_api.get_waiver_wire_players(access_token, league_key)
    
    # 2. Transform the raw XML elements into a list of Pydantic objects
    waiver_players = []
    for player_element in raw_player_elements:
        try:
            player_data = _parse_player_element(player_element)
            waiver_players.append(player_data)
        except (ValueError, TypeError) as e:
            # Log the error for the specific player and continue
            # In a real app, you'd use a proper logger.
            print(f"Skipping player due to parsing error: {e}")
            continue
            
    return waiver_players
