#!/usr/bin/python3
"""LFU caching"""
from typing import Any

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU caching system"""

    def __init__(self) -> None:
        """ Initialize of LFU and call the base"""
        super().__init__()
        self.key_frequency = {}

    def put(self, key, item) -> None:
        """ Store the data in LFU policy"""
        if not key or not item:
            return

        if key in self.cache_data.keys():
            self.cache_data[key] = item

            self.key_frequency[key] += 1
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            min_key = min(self.key_frequency, key=self.key_frequency.get)
            self.cache_data.pop(min_key)
            self.key_frequency.pop(min_key)
            print(f'DISCARD: {min_key}')

        self.key_frequency[key] = 1
        self.cache_data[key] = item

    def get(self, key) -> Any:
        """ Get data from LFU cache system"""
        value = self.cache_data.get(key)
        if value:
            self.key_frequency[key] += 1

        return self.cache_data.get(key, None)
