# ==============================================================================
# Module: xcachelib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library for maintaining the runserver data cache.
# Notes:
# ==============================================================================

import json
import threading
from cachetools import TTLCache
from datetime import datetime

class ThreadSafeJSONCache:
    def __init__(self, maxsize=1000, ttl=600):
        """
        Initializes a thread-safe cache.
        :param maxsize: Maximum size of the cache.
        :param ttl: Time to live for each cache item in seconds.
        """
        # Create a TTLCache and wrap it with RLock for thread safety
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.lock = threading.RLock()

    def write(self, name, value, status):
        """
        Writes a name-value pair to the cache, where value is a JSON object.
        :param name: The name (key) under which the data is stored.
        :param value: The value to be stored.
        :param status: The status associated with the value.
        """
        with self.lock:  # Ensuring thread safety with a context manager
            time_stamp = datetime.now().isoformat()
            self.cache[name] = json.dumps({"time": time_stamp, "value": value, "status": status})

    def read(self, name):
        """
        Reads the value associated with a name from the cache.
        :param name: The name (key) of the data to be retrieved.
        :return: The JSON object associated with the name, or None if not found.
        """
        with self.lock:  # Ensuring thread safety with a context manager
            return self.cache.get(name, None)

# Instantiate class to make it a singleton instance
data_cache_instance = ThreadSafeJSONCache(maxsize=10000, ttl=600)

# Example usage
#if __name__ == "__main__":
#    cache = ThreadSafeJSONCache(maxsize=10, ttl=600)  # Initialize cache with maxsize 10 and TTL 10 minutes

    # Writing data to cache
#    cache.write("example_key", "example_value", "OK")

    # Reading data from cache
#    cached_data = cache.read("example_key")
#    if cached_data:
#        print("Cached Data:", cached_data)
#    else:
#        print("No data found for key.")
