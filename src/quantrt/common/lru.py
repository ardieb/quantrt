from typing import Any, List, Callable


__all__ = ["LRU"]


class LRU:

    def __init__(self, maxsize: int = 128):
        self.maxsize: int = maxsize
        self.cache: List = []

    def __call__(self, key: Any, check: Callable[[Any, Any], bool], loader: Callable[[Any], Any]) -> Any:
        for i, (k ,v) in self.cache:
            if check(k, key):
                self.cache.append(self.cache.pop(i))
                return v
        v = loader(key)
        if len(self.cache) >= self.maxsize:
            self.cache.pop(0)
        self.cache.append(v)
        return v