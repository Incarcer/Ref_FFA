import time
from typing import Dict
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app import crud, models, schemas
from app.api import deps
from app.core.db import get_db
from app.core.config import settings
from app.services import yahoo_service

router = APIRouter()

@router.get("/yahoo/auth", response_model=schemas.yahoo_token.AuthURL)
def get_yahoo_auth_url(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Generate the Yahoo authorization URL for the user to visit.
    This now returns JSON instead of a direct redirect.
    """
    authorization_url = yahoo_service.get_authorization_url(user_id=current_user.id)
    return {"authorization_url": authorization_url}

@router.get("/yahoo/callback")
async def handle_yahoo_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Handles the redirect from Yahoo after user authorization.
    Validates state, exchanges the code for tokens, and saves them.
    """
    try:
        payload = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "state":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid state token type")
        
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired state token.")

    try:
        token_info = await yahoo_service.exchange_code_for_token(code)
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authorization code or failed to exchange for token.",
        )

    token_in = schemas.yahoo_token.YahooTokenCreate(
        access_token=token_info["access_token"],
        refresh_token=token_info["refresh_token"],
        token_type=token_info["token_type"],
        expires_at=int(time.time()) + token_info["expires_in"],
    )

    crud.crud_yahoo_token.create_or_update(db, obj_in=token_in, user_id=user_id)

    # Redirect user back to the leagues page in the frontend
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/leagues")

@router.get("/yahoo/status", response_model=schemas.yahoo_token.YahooAuthStatus)
def get_yahoo_link_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Check if the current user has linked their Yahoo account."""
    token = crud.crud_yahoo_token.get_by_user_id(db, user_id=current_user.id)
    return {"is_linked": token is not None}

@router.get("/yahoo/leagues", response_model=schemas.yahoo_token.YahooLeaguesResponse)
async def fetch_user_leagues(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Fetch the authenticated user's fantasy leagues from Yahoo."""
    leagues = await yahoo_service.get_user_leagues(db, user_id=current_user.id)
    return {"leagues": leagues}