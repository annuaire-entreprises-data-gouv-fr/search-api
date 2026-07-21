# from redis import asyncio as redis
import logging

import redis

from app.config import settings


class Singleton(type):
    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    def __init__(self):
        host = settings.redis.host
        port = settings.redis.port
        db = settings.redis.database

        # Connecting to redis client
        try:
            self.server = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                health_check_interval=30,
            )
            ping = self.server.ping()
            if not ping:
                logging.error(f"**************Could not ping Redis: {ping}")
        except redis.exceptions.RedisError as error:
            logging.info(f"Redis error while connecting: {error}")

    def get(self, key):
        try:
            cached_value = self.server.get(key)
            return cached_value
        except redis.RedisError as error:
            logging.info(f"Error while getting value using key: {error}")

    def set(
        self,
        key,
        value,
        expire,
    ):
        try:
            self.server.set(key, value, ex=expire)
        except redis.RedisError as error:
            logging.info(f"Error while saving value: {error}")
