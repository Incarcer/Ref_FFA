import requests
import xml.etree.ElementTree as ET
from typing import List, Optional
from fastapi import HTTPException

YAHOO_API_BASE_URL = "https://fantasysports.yahooapis.com/fantasy/v2"

def _make_api_request(url: str, access_token: str) -> ET.Element:
    """
    Makes a request to the Yahoo Fantasy API.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Yahoo's API returns XML, so we parse it.
        return ET.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        # In a real app, you'd have more robust error handling and logging
        raise HTTPException(status_code=400, detail=f"Error contacting Yahoo API: {e}")
    except ET.ParseError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Yahoo API response: {e}")

def get_user_leagues(access_token: str) -> ET.Element:
    """
    Fetches all fantasy football leagues for the authenticated user.
    This is a placeholder for existing functionality.
    """
    url = f"{YAHOO_API_BASE_URL}/users;use_login=1/games;game_keys=nfl/leagues"
    return _make_api_request(url, access_token)

def get_waiver_wire_players(access_token: str, league_key: str) -> List[ET.Element]:
    """
    Fetches players available on the waiver wire for a specific league.
    
    The 'status=W' filter gets players currently on waivers.
    You could also use 'status=FA' for free agents or 'status=A' for all available.
    """
    # We can fetch sub-resources like editorial_player_key, and percent_owned
    # to avoid making individual requests for each player later.
    url = f"{YAHOO_API_BASE_URL}/league/{league_key}/players;status=W/stats"
    
    root = _make_api_request(url, access_token)
    
    # XML from Yahoo API has namespaces, which we need to handle.
    namespace = {'y': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng'}
    
    # Find all 'player' elements within the XML structure.
    players = root.findall('.//y:player', namespace)
    
    return players
