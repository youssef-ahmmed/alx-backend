#!/usr/bin/python3
"""LRU caching"""
from typing import Any

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU caching system"""

    def __init__(self) -> None:
        """ Initialize of LRU and call the base"""
        super().__init__()
        self.lru_keys = []

    def put(self, key, item) -> None:
        """ Store the data in LRU policy"""
        if not key or not item:
            return

        if key in self.lru_keys:
            self.cache_data[key] = item

            self.lru_keys.remove(key)
            self.lru_keys.append(key)
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            self.cache_data.pop(self.lru_keys[0])
            print(f'DISCARD: {self.lru_keys[0]}')
            self.lru_keys.pop(0)

        self.lru_keys.append(key)
        self.cache_data[key] = item

    def get(self, key) -> Any:
        """ Get data from LRU cache system"""
        value = self.cache_data.get(key)
        if value:
            self.lru_keys.remove(key)
            self.lru_keys.append(key)

        return self.cache_data.get(key, None)
