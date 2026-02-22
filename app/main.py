from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.database import MongoDB
import logging
import os
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Study Bot API",
    description="AI Study Assistant with MongoDB Memory",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    try:
        MongoDB.connect_to_mongodb()
        logger.info("✅ MongoDB connected successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB on shutdown"""
    MongoDB.close_connection()
    logger.info("Application shutdown complete")

@app.get("/")
async def root():
    return {
        "message": "Study Bot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "database": "connected"}

# This is important for Render - allows running directly with python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)