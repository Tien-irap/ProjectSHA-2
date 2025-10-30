import hashlib
from fastapi import UploadFile, HTTPException
from datetime import datetime
from typing import List, Dict, Any

from ..core.db_connection import collection
from ..models.schemas import TextHashRequest, HashRecord

# --- Core Hashing Functions ---

def hash_text(text: str, algorithm: str = 'sha256') -> str:
    """Hashes a string using the specified SHA-2 algorithm."""
    
    # Get the hash function from hashlib
    # We use .new() to dynamically select the algorithm
    try:
        hash_func = hashlib.new(algorithm)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid hash algorithm. Use sha224, sha256, sha384, or sha512.")
    
    # Encode the text to bytes and update the hash
    hash_func.update(text.encode('utf-8'))
    
    # Return the hexadecimal digest
    return hash_func.hexdigest()

def hash_file_chunks(file: UploadFile, algorithm: str = 'sha256') -> str:
    """
    Hashes a file by reading it in chunks to handle large files 
    efficiently without consuming all the memory.
    """
    try:
        hash_func = hashlib.new(algorithm)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid hash algorithm. Use sha224, sha256, sha384, or sha512.")

    # Read the file in 4MB chunks
    while chunk := file.file.read(4096 * 1024):
        hash_func.update(chunk)
    
    # Reset file pointer to the beginning in case it's needed again
    file.file.seek(0) 
    
    return hash_func.hexdigest()

def hash_file_content(file: UploadFile, algorithm: str) -> str:
    """Helper function to hash file content without storing it."""
    hasher = hashlib.new(algorithm)
    # Read file in chunks to handle large files efficiently
    while chunk := file.file.read(8192):
        hasher.update(chunk)
    # Reset file pointer to the beginning in case it needs to be read again
    file.file.seek(0)
    return hasher.hexdigest()

def verify_file_hash(file: UploadFile, known_hash: str, algorithm: str) -> bool:
    """
    Hashes an uploaded file and compares it to a known hash.
    Returns True if they match, False otherwise.
    """
    # Calculate the hash of the newly uploaded file
    calculated_hash = hash_file_content(file, algorithm)
    
    # Compare the calculated hash with the provided known hash
    # Use a case-insensitive comparison as hash formats can vary
    return calculated_hash.lower() == known_hash.lower()

# --- Database Interaction Functions ---

def create_and_store_text_hash(request: TextHashRequest) -> str:
    """Hashes text and stores the record in the database."""
    calculated_hash = hash_text(request.text, request.algorithm)

    record = {
        "input_type": "text",
        "original_input": request.text, # Security Warning: Not for production
        "algorithm": request.algorithm,
        "hash": calculated_hash,
        "timestamp": datetime.utcnow()
    }
    
    collection.insert_one(record)
    return calculated_hash

def create_and_store_file_hash(file: UploadFile, algorithm: str) -> str:
    """Hashes a file and stores the record in the database."""
    calculated_hash = hash_file_chunks(file, algorithm)

    record = {
        "input_type": "file",
        "original_filename": file.filename,
        "algorithm": algorithm,
        "hash": calculated_hash,
        "timestamp": datetime.utcnow()
    }
    
    collection.insert_one(record)
    return calculated_hash

def retrieve_all_hashes(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves all hash records from the database, sorted by most recent."""
    records = []
    # Find all records, sort by most recent, limit
    for doc in collection.find().sort("timestamp", -1).limit(limit):
        doc["_id"] = str(doc["_id"]) # Convert ObjectId to string for JSON
        records.append(doc)
    return records