from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.database import MongoDB
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI application
app = FastAPI(
    title="Study Bot API",
    description="AI Study Assistant with MongoDB Memory",
    version="1.0.0"
)

# Allow any website to use our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # * means allow everyone
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect our chat routes
app.include_router(chat.router)

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up when app stops"""
    MongoDB.close_connection()
    logger.info("Application shutdown complete")

@app.get("/")
async def root():
    """Homepage - shows API is working"""
    return {
        "message": "Study Bot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Check if API is alive"""
    return {"status": "healthy"}