from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from ..core.db_connection import get_db
from ..models.user_models import UserCreate, UserInDB

# --- Configuration ---
# Use a secure, randomly generated string for this in a real application
# You can generate one using: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# --- User Database Operations ---
def get_user(username: str) -> Optional[UserInDB]:
    """Retrieves a user from the database by username."""
    db = get_db()
    user_data = db.users.find_one({"username": username})
    if user_data:
        return UserInDB(**user_data)
    return None

def create_user(user: UserCreate) -> UserInDB:
    """Creates a new user in the database."""
    db = get_db()
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed_password)
    
    # Convert Pydantic model to dict for MongoDB insertion
    user_dict = user_in_db.dict()
    
    db.users.insert_one(user_dict)
    return user_in_db

# --- JWT Token Handling ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt