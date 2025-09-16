import time
import logging
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import create_state_token
from app.schemas.yahoo_token import YahooTokenCreate, YahooLeague

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
YAHOO_BASE_URL = "https://fantasysports.yahooapis.com/fantasy/v2"
AUTHORIZATION_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
YAHOO_XML_NAMESPACE = {'y': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng'}

def get_authorization_url(user_id: int) -> str:
    """Constructs the Yahoo authorization URL with a secure state token."""
    state = create_state_token(subject=user_id)
    params = {
        "client_id": settings.YAHOO_CLIENT_ID,
        "redirect_uri": settings.YAHOO_REDIRECT_URI,
        "response_type": "code",
        "state": state,
    }
    return f"{AUTHORIZATION_URL}?{urlencode(params)}"

async def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """Exchanges an authorization code for an access and refresh token."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": settings.YAHOO_CLIENT_ID,
        "client_secret": settings.YAHOO_CLIENT_SECRET,
        "redirect_uri": settings.YAHOO_REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

async def refresh_token(refresh_token: str) -> Dict[str, Any]:
    """Refreshes an expired access token."""
    data = {
        "client_id": settings.YAHOO_CLIENT_ID,
        "client_secret": settings.YAHOO_CLIENT_SECRET,
        "redirect_uri": settings.YAHOO_REDIRECT_URI,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

async def get_refreshed_token(db: Session, user_id: int) -> str:
    """
    Retrieves a user's token, refreshing it if necessary, and returns a valid access token.
    """
    token_data = crud.crud_yahoo_token.get_by_user_id(db, user_id=user_id)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yahoo account not linked.")

    if token_data.expires_at < time.time() - 60:
        try:
            new_token_info = await refresh_token(token_data.refresh_token)
            token_in = YahooTokenCreate(
                access_token=new_token_info["access_token"],
                refresh_token=new_token_info.get("refresh_token", token_data.refresh_token),
                token_type=new_token_info["token_type"],
                expires_at=int(time.time()) + new_token_info["expires_in"],
            )
            crud.crud_yahoo_token.create_or_update(db, obj_in=token_in, user_id=user_id)
            return token_in.access_token
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to refresh Yahoo token for user {user_id}: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to refresh Yahoo token.")
    
    return token_data.access_token

async def get_user_leagues(db: Session, user_id: int) -> List[YahooLeague]:
    """Fetches a user's fantasy football leagues from the Yahoo API."""
    access_token = await get_refreshed_token(db, user_id=user_id)
    url = f"{YAHOO_BASE_URL}/users;use_login=1/games;game_keys=nfl/leagues"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"Error fetching leagues from Yahoo for user {user_id}: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching leagues from Yahoo.")

    root = ET.fromstring(response.content)
    leagues = []
    for league_elem in root.findall('.//y:league', YAHOO_XML_NAMESPACE):
        try:
            league = YahooLeague(
                league_key=league_elem.find('y:league_key', YAHOO_XML_NAMESPACE).text,
                name=league_elem.find('y:name', YAHOO_XML_NAMESPACE).text,
                url=league_elem.find('y:url', YAHOO_XML_NAMESPACE).text,
                season=int(league_elem.find('y:season', YAHOO_XML_NAMESPACE).text),
            )
            leagues.append(league)
        except (AttributeError, ValueError) as e:
            logger.warning(f"Skipping malformed league element during XML parsing: {e}")
            continue
    return leagues