from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ..services import auth_logic
from ..models import user_models

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=user_models.UserBase, status_code=status.HTTP_201_CREATED)
async def register_user(user: user_models.UserCreate):
    """
    Registers a new user.
    - Hashes the password using passlib.
    - Stores the username and hashed password in MongoDB.
    """
    db_user = auth_logic.get_user(user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    created_user = auth_logic.create_user(user)
    return user_models.UserBase(username=created_user.username)

@router.post("/login", response_model=user_models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logs in a user and returns a JWT access token.
    - Verifies username and password.
    - Returns a JWT token upon success.
    """
    user = auth_logic.get_user(form_data.username)
    if not user or not auth_logic.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_logic.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_logic.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}