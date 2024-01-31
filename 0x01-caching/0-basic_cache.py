#!/usr/bin/python3
"""Basic dictionary"""
from typing import Any

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ Basic caching system
    """

    def put(self, key, item) -> None:
        if item is None:
            return
        self.cache_data[key] = item

    def get(self, key) -> Any:
        if key:
            return self.cache_data.get(key, None)
