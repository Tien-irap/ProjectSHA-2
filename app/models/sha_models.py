from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Pydantic Models for Request Data ---
class TextHashRequest(BaseModel):
    text: str
    algorithm: str = "sha256"

# --- Pydantic Models for Response Data ---
class TextHashResponse(BaseModel):
    original_text: str
    algorithm: str
    hash: str

class FileHashResponse(BaseModel):
    filename: str
    content_type: Optional[str]
    algorithm: str
    hash: str

class HashRecord(BaseModel):
    id: str = Field(..., alias="_id")
    input_type: str
    original_input: Optional[str] = None
    original_filename: Optional[str] = None
    algorithm: str
    hash: str
    timestamp: datetime

class HashCheckResponse(BaseModel):
    """Response model for the hash comparison check."""
    match: bool
    message: str