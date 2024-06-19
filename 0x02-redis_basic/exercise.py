"""
    exercise.py
"""
import redis
import uuid
from typing import Union, Optional, Callable
import functools


class Cache:
    def __init__(self) -> None:
        """
            Initialization
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """
            Count how many times methods of the Cache class are called.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return wrapper

    def call_history(method: Callable) -> Callable:
        """
            Store the history of inputs and outputs for a particular function
        """
        @functools.wraps(method)
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

    def get(self, key: str, fn: Optional[Callable]) -> Union[str, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
            Parametrize Cache.get with the correct conversion function
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: int) -> Optional[int]:
        """
            Parametrize Cache.get with the correct conversion function
        """
        return self.get(key, lambda x: int(x))

    def replay(self, method: Callable) -> None:
        """
            Display the history of calls of a particular function
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self = method.__self__

        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")

        for input_data, output_data in zip(inputs, outputs):
            input_str = input_data.decode('utf-8')
            output_str = output_data.decode('utf-8')
            print(f"{method.__qualname__}(*{input_str}) -> {output_str}")
