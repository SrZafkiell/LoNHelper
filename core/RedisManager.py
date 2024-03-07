import redis

from core.ConfigManager import ConfigManager
# Object that contains all the config data from the config.json file
config = ConfigManager()


class RedisManager:
    def __init__(self, num_connections, **redis_kwargs):
        """
        Initialize the Redis connection pool with the specified number of connections.
        The `redis_kwargs` argument is a dictionary of keyword arguments to pass to the Redis
        constructor.
        """
        self.redis_pool = redis.ConnectionPool(**redis_kwargs, max_connections=num_connections)

    def get_connection(self):
        """
        Get a connection from the Redis connection pool.
        """
        return redis.StrictRedis(connection_pool=self.redis_pool, decode_responses=True)

    def close_all_connections(self):
        """
        Close all connections in the Redis connection pool.
        """
        self.redis_pool.disconnect()
