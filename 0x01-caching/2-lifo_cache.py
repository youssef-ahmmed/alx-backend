#!/usr/bin/python3
"""LIFO caching"""
from typing import Any

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching system"""

    def __init__(self) -> None:
        """ Initialize of LIFO and call the base"""
        super().__init__()
        self.stack = []

    def put(self, key, item) -> None:
        """ Store the data in LIFO policy"""
        if key is None or item is None:
            return

        if key in self.stack:
            self.cache_data[key] = item

            self.stack.remove(key)
            self.stack.append(key)
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            discard_key = self.stack.pop()
            self.cache_data.pop(discard_key, None)
            print(f'DISCARD: {discard_key}')

        self.stack.append(key)
        self.cache_data[key] = item

    def get(self, key) -> Any:
        """ Get data from a LIFO cache system"""
        return self.cache_data.get(key, None)
