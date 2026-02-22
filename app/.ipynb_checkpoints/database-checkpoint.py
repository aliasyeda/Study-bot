from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    client: MongoClient = None
    database = None
    
    @classmethod
    def connect_to_mongodb(cls):
        """Connect to MongoDB"""
        try:
            # Create connection to MongoDB
            cls.client = MongoClient(settings.MONGODB_URI)
            cls.database = cls.client[settings.DATABASE_NAME]
            
            # Test if connection works
            cls.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully!")
            
            # Create indexes for faster searching
            cls.database[settings.COLLECTION_NAME].create_index("session_id")
            cls.database[settings.COLLECTION_NAME].create_index("timestamp")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection when app stops"""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")

# Auto-connect when this file is imported
MongoDB.connect_to_mongodb()