#!/usr/bin/env python3
"""
This model for redis client
"""
import redis
from os import getenv


class RedisClient:
    """define class RedisClient"""

    def __init__(self):
        HOST = getenv("REDIS_HOST", "localhost")
        PORT = getenv("REDIS_PORT", 6379)
        self.client = redis.Redis(host=HOST, port=PORT)
        self.is_connected = True

        try:
            self.client.ping()
        except redis.ConnectionError as err:
            print(f'Redis client not connected to the server: {err}')
            self.is_connected = False

    def is_alive(self):
        """
        Check if client is connected or not.
        Returns: Boolean
        """
        return self.is_connected

    def get(self, key):
        """
        Retrieves the value of a given key.
        Args:
            key: The key of the item to retrieve.
        Returns: The value of the key.
        """
        try:
            return self.client.get(key)
        except redis.RedisError as err:
            print(f"Error getting key {key}: {err}")
            return None

    def set(self, key, value, duration):
        """
        Set key value with duration in seconds.
        Args:
            key: The key of the item to store.
            value: The value of the item to store.
            duration: The expiration time of the item in seconds.
        """
        try:
            self.client.setex(key, duration, value)
        except redis.RedisError as err:
            print(f"Error setting key {key}: {err}")

    def delete(self, key):
        """
        Delete an item that is stored.
        Args:
            key: The key of the item.
        """
        try:
            self.client.delete(key)
        except redis.RedisError as err:
            print(f"Error deleting key {key}: {err}")
