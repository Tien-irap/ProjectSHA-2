from fastapi import FastAPI
from .routes import sha_routes 
from .routes import auth_routes
from .routes import websocket_routes
from .core.websockets_connection import manager


app = FastAPI(
    title="SHA-2 Hashing Service",
    description="A project to demonstrate SHA-2 hashing with FastAPI and MongoDB."
)

# Include the API routes from the routes module
app.include_router(sha_routes.router, prefix="/api") # Added a prefix for better organization
app.include_router(auth_routes.router)
app.include_router(websocket_routes.router)
