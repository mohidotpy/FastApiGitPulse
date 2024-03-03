from abc import ABC, abstractmethod


class CacheRepository(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str, ttl: int):
        pass


class RedisRepository(CacheRepository):
    def __init__(self, redis_connection):
        self.redis_client = redis_connection

    def get(self, key: str):
        return self.redis_client.get(key)

    def set(self, key: str, value: str, ttl: int):
        self.redis_client.set(key, value, ex=ttl)
