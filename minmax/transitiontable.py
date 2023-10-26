""" Module containing an implementation of data structures for a transition table."""
from  collections import OrderedDict

class LRUCacheWithDefault:
    """Class for a Least Recently Used Cache with a default function."""
    def __init__(self, capacity: int, default_func: callable):
        self.capacity = capacity
        self.default_func = default_func
        self.cache = OrderedDict()

    def __getitem__(self, key: int) -> int:
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return self.default_func()

    def __setitem__(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def __delitem__(self, key: int) -> None:
        """Remove the specified key and its associated value."""
        if key in self.cache:
            self.cache.pop(key)