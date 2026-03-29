import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

# Create connection
client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)

# Database
db = client["crypto_ai"]

# Collections
reports_collection = db["reports"]

# Verify connection at startup
try:
    client.admin.command("ping")
    logger.info("✅ MongoDB connected successfully")
except ConnectionFailure as e:
    logger.error(f"❌ MongoDB connection FAILED: {e}")