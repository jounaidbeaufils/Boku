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

class LRUCache:
    """Class for a Least Recently Used Cache. Taken from the the following URL:
    https://www.geeksforgeeks.org/lru-cache-in-python-using-ordereddict/
    """
    # initialising capacity
    def __init__(self, capacity: int, default_func: callable):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.default_func = default_func

    def get(self, key: int) -> int:
        """ Returns the value of the specified key in the cache."""
        if key not in self.cache:
            return self.default_func()
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """Sets the value of the specified key in the cache."""
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)
