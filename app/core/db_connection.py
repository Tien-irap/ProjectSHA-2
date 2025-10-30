# --- MongoDB Connection ---
import pymongo
import os

# For local development with MongoDB Compass, you might use:
# MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
# For production or cloud deployments, it's highly recommended to use environment variables.
# Example: MONGO_CONNECTION_STRING = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_CONNECTION_STRING = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "sha2_project"
COLLECTION_NAME = "hash_records"

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_db():
    """Returns the MongoDB database instance."""
    return db