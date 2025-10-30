from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    """Base model for a user, containing the username."""
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    """Schema for creating a new user. Includes the password."""
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    """Schema for user data as stored in the database, including the hashed password."""
    hashed_password: str

class Token(BaseModel):
    """Schema for the access token returned upon successful login."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the data encoded within a JWT."""
    username: Optional[str] = None