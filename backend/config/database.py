"""
MongoDB database connection and utilities.
Handles async MongoDB operations using Motor.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from loguru import logger

from .settings import settings


class Database:
    """MongoDB database connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect(cls) -> None:
        """Establish connection to MongoDB."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_uri)
            cls.db = cls.client[settings.mongodb_db_name]
            
            # Test the connection
            await cls.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.mongodb_db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def disconnect(cls) -> None:
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("Disconnected from MongoDB")
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get the database instance."""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls.db
    
    @classmethod
    async def store_analysis(cls, analysis_id: str, data: dict) -> str:
        """
        Store financial analysis result in MongoDB.
        
        Args:
            analysis_id: Unique identifier for the analysis
            data: Complete analysis JSON
            
        Returns:
            Inserted document ID
        """
        db = cls.get_database()
        collection = db[settings.mongodb_collection]
        
        document = {
            "analysis_id": analysis_id,
            "data": data,
            "created_at": data.get("created_at"),
        }
        
        result = await collection.insert_one(document)
        logger.info(f"Stored analysis {analysis_id} in MongoDB")
        
        return str(result.inserted_id)
    
    @classmethod
    async def get_analysis(cls, analysis_id: str) -> Optional[dict]:
        """
        Retrieve financial analysis by ID.
        
        Args:
            analysis_id: Unique identifier for the analysis
            
        Returns:
            Analysis document or None if not found
        """
        db = cls.get_database()
        collection = db[settings.mongodb_collection]
        
        document = await collection.find_one({"analysis_id": analysis_id})
        
        if document:
            logger.info(f"Retrieved analysis {analysis_id} from MongoDB")
            return document.get("data")
        
        return None


# Global database instance
database = Database()
