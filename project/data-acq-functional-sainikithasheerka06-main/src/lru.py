#!/usr/bin/env python3
from typing import Any, Optional

from collections import OrderedDict 

class LRUCache:
    """
    A Least Recently Used (LRU) cache keeps items in the cache until it reaches its size
    and/or item limit (only item in our case). In which case, it removes an item that was accessed
    least recently.
    An item is considered accessed whenever `has`, `get`, or `set` is called with its key.

    Implement the LRU cache here and use the unit tests to check your implementation.
    """

    def __init__(self, item_limit: int):
        # TODO: implement this function
        self._limit = max(0, int(item_limit))
        self._data: "OrderedDict[str, Any]" = OrderedDict()

    def has(self, key: str) -> bool:
        # TODO: implement this function
        exists = key in self._data                     
        if exists:                                     
            self._data.move_to_end(key, last=True)     
        return exists

    def get(self, key: str) -> Optional[Any]:
        # TODO: implement this function
        if key in self._data:                          
            self._data.move_to_end(key, last=True)     
            return self._data[key]                     
        return None

    def set(self, key: str, value: Any):
        # TODO: implement this function
        if self._limit == 0:                       
            return                                   
        self._data[key] = value                     
        self._data.move_to_end(key, last=True)       
        while len(self._data) > self._limit:          
            self._data.popitem(last=False)
