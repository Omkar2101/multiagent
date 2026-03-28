import redis
from app.core.config import settings

# Create Redis client (connection to Redis server)
redis_client = redis.Redis(
    host="localhost",   # Redis server location
    port=6379,          # Default Redis port
    db=0,               # Database index
    decode_responses=True  # Important: auto convert bytes → string
)