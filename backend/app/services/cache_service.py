import json
import logging
from app.core.cache import redis_client

logger = logging.getLogger(__name__)


class CacheService:

    # -------------------------------
    # GET data from cache
    # -------------------------------
    @staticmethod
    def get(key: str):
        """
        Fetch data from Redis cache
        """
        logger.info(f"[Redis] GET {key}")
        try:
            data = redis_client.get(key)
            if data:
                logger.info(f"[Redis] ✅ Cache HIT for {key}")
                try:
                    return json.loads(data)
                except Exception:
                    return data
            logger.info(f"[Redis] Cache MISS for {key}")
            return None
        except Exception as e:
            logger.error(f"[Redis] ❌ GET failed for {key}: {e}")
            return None


    # -------------------------------
    # SET data with TTL
    # -------------------------------
    @staticmethod
    def set(key: str, value, ttl: int = 300):
        """
        Store data in Redis with expiration time
        """
        logger.info(f"[Redis] SET {key} (ttl={ttl}s)")
        try:
            redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            logger.info(f"[Redis] ✅ Cached {key}")
        except Exception as e:
            logger.error(f"[Redis] ❌ SET failed for {key}: {e}")


    # -------------------------------
    # DELETE cache
    # -------------------------------
    @staticmethod
    def delete(key: str):
        """
        Remove cache manually
        """
        logger.info(f"[Redis] DELETE {key}")
        redis_client.delete(key)


    # -------------------------------
    # CHECK if key exists
    # -------------------------------
    @staticmethod
    def exists(key: str) -> bool:
        return redis_client.exists(key) == 1