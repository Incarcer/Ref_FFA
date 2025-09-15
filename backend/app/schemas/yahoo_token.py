from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List

# --- Token Schemas ---
class YahooTokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: int  # Unix timestamp

class YahooTokenCreate(YahooTokenBase):
    pass

class YahooTokenInDB(YahooTokenBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

# --- API Response Schemas ---
class AuthURL(BaseModel):
    authorization_url: HttpUrl

class YahooAuthStatus(BaseModel):
    is_linked: bool

class YahooLeague(BaseModel):
    league_key: str
    name: str
    url: HttpUrl
    season: int

class YahooLeaguesResponse(BaseModel):
    leagues: List[YahooLeague]