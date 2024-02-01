#!/usr/bin/python3
"""MRU caching"""
from typing import Any

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU caching system"""

    def __init__(self) -> None:
        """ Initialize of MRU and call the base"""
        super().__init__()
        self.last_key = None

    def put(self, key, item) -> None:
        """ Store the data in MRU policy"""
        if not key or not item:
            return

        if key in self.cache_data.keys():
            self.cache_data[key] = item

            self.last_key = key
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            discard_key = self.last_key
            self.cache_data.pop(discard_key)
            print(f'DISCARD: {discard_key}')

        self.last_key = key
        self.cache_data[key] = item

    def get(self, key) -> Any:
        """ Get data from MRU cache system"""
        value = self.cache_data.get(key)
        if value:
            self.last_key = key

        return self.cache_data.get(key, None)
