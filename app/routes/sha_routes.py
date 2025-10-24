from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List

from ..services import sha_logic
from ..models.sha_model import TextHashRequest, TextHashResponse, FileHashResponse, HashRecord

router = APIRouter()

@router.get("/", summary="Welcome Message")
async def root():
    """A simple welcome message."""
    return {"message": "Welcome to the SHA-2 Hashing API"}

@router.post("/hash/text/", response_model=TextHashResponse, summary="Hash a Text String")
async def create_text_hash(request: TextHashRequest) -> TextHashResponse:
    """
    Hashes a simple text string (like a password or message).
    Stores the original text and its hash in MongoDB.
    """
    try:
        # The service function handles hashing and DB insertion
        calculated_hash = sha_logic.create_and_store_text_hash(request)
        return TextHashResponse(
            original_text=request.text,
            algorithm=request.algorithm,
            hash=calculated_hash
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hash/file/", response_model=FileHashResponse, summary="Hash an Uploaded File")
async def create_file_hash(
    file: UploadFile = File(...), 
    algorithm: str = "sha256"
) -> FileHashResponse:
    """
    Hashes an uploaded file.
    Stores the filename and its hash in MongoDB.
    """
    try:
        calculated_hash = sha_logic.create_and_store_file_hash(file, algorithm)
        return FileHashResponse(
            filename=file.filename,
            content_type=file.content_type,
            algorithm=algorithm,
            hash=calculated_hash
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hashes/", response_model=List[HashRecord], summary="Retrieve Recent Hashes")
async def get_all_hashes() -> List[HashRecord]:
    """
    Retrieves all hash records from the MongoDB database.
    """
    return sha_logic.retrieve_all_hashes()