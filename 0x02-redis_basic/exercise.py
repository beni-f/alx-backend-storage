"""
    exercise.py
"""
import redis
import uuid
from typing import Union, Optional, Callable
import functools


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int, float]]] = None) -> Union[str, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data
    
    def get_str(self, key:str) -> Optional[str]:
        return self.get(key, lambda x: x.decode('utf-8'))
    
    def get_int(self, key:int) -> Optional[int]:
        return self.get(key, lambda x: int(x))
