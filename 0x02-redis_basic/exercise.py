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
    
    def call_history(method: Callable) -> Callable:
        @functools.wrap(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"

            self._redis.rpush(input_key, str(args))

            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(output))

            return output
        return wrapper

    @call_history
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
