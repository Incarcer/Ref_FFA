from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException

# NOTE: The following imports are based on common project structures and assumptions
# about where authentication dependencies are located. The exact paths may need
# to be adjusted to match the project's actual implementation.
from backend.app.dependencies import get_current_active_user
from backend.app.schemas.user import User
from backend.app.schemas.waiver import WaiverPlayer
from backend.app.services import waiver_service

router = APIRouter()

@router.get(
    "/waiver-wire",
    response_model=List[WaiverPlayer],
    summary="Get Waiver Wire Players",
    description="Fetches a list of players currently available on the waiver wire for a given league. The league_key must be provided in the path prefix when this router is included in the main app."
)
def read_waiver_wire(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieves waiver wire players from the Yahoo Fantasy API for a specific league.
    The `league_key` is extracted from the URL path parameters.
    Requires an authenticated user with a valid Yahoo access token.
    """
    if "league_key" not in request.path_params:
        raise HTTPException(status_code=400, detail="League key missing in URL path.")

    league_key = request.path_params["league_key"]
    
    if not hasattr(current_user, 'yahoo_access_token') or not current_user.yahoo_access_token:
        raise HTTPException(
            status_code=401, 
            detail="User not authenticated with Yahoo or access token is missing."
        )

    waiver_players = waiver_service.process_waiver_data(
        access_token=current_user.yahoo_access_token, 
        league_key=league_key
    )
    return waiver_players
