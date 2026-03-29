import logging
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Redis client (connection to Redis server)
redis_client = redis.Redis(
    host="localhost",   # Redis server location
    port=6379,          # Default Redis port
    db=0,               # Database index
    decode_responses=True  # Important: auto convert bytes → string
)

# Verify connection at startup
try:
    redis_client.ping()
    logger.info("✅ Redis connected successfully")
except redis.exceptions.ConnectionError as e:
    logger.error(f"❌ Redis connection FAILED: {e}")