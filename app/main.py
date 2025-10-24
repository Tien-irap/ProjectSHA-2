from fastapi import FastAPI
from .routes import sha_routes

app = FastAPI(
    title="SHA-2 Hashing Service",
    description="A project to demonstrate SHA-2 hashing with FastAPI and MongoDB."
)

# Include the API routes from the routes module
app.include_router(sha_routes.router)