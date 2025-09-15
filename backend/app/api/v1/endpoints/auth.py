from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.api import deps
from app.core import security
from app.core.db import get_db
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.user.UserPublic)
def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticates user and sets an HttpOnly access token cookie.
    """
    user = crud.crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token_cookie",
        value=access_token,
        httponly=True,
        max_age=int(access_token_expires.total_seconds()),
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    return user

@router.post("/register", response_model=schemas.user.UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(
    db: Session = Depends(get_db),
    user_in: schemas.user.UserCreate = Depends(),
):
    """Create new user."""
    user = crud.crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists.",
        )
    new_user = crud.crud_user.create_user(db=db, user_in=user_in)
    return new_user

@router.post("/logout")
def logout(response: Response):
    """Logs out the user by clearing the access token cookie."""
    response.delete_cookie("access_token_cookie")
    return {"message": "Successfully logged out"}

@router.get("/users/me", response_model=schemas.user.UserPublic)
def read_users_me(current_user: models.User = Depends(deps.get_current_active_user)):
    """Get current user."""
    return current_user