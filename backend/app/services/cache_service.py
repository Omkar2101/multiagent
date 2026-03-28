import json
from app.core.cache import redis_client


class CacheService:

    # -------------------------------
    # GET data from cache
    # -------------------------------
    @staticmethod
    def get(key: str):
        """
        Fetch data from Redis cache
        """

        data = redis_client.get(key)

        if data:
            try:
                return json.loads(data)  # Convert string → dict
            except:
                return data

        return None


    # -------------------------------
    # SET data with TTL
    # -------------------------------
    @staticmethod
    def set(key: str, value, ttl: int = 300):
        """
        Store data in Redis with expiration time

        key: unique identifier
        value: any Python object
        ttl: time in seconds
        """

        try:
            redis_client.setex(
                key,
                ttl,
                json.dumps(value)  # Convert dict → string
            )
        except Exception as e:
            print("Redis SET Error:", e)


    # -------------------------------
    # DELETE cache
    # -------------------------------
    @staticmethod
    def delete(key: str):
        """
        Remove cache manually
        """
        redis_client.delete(key)


    # -------------------------------
    # CHECK if key exists
    # -------------------------------
    @staticmethod
    def exists(key: str) -> bool:
        return redis_client.exists(key) == 1