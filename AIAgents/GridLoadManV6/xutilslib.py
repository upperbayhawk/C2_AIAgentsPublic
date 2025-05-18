# ==============================================================================
# Module: xutilslib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library for maintaining the runserver data cache.
# Notes:
# ==============================================================================
import json
import os
import re
import threading
import time
from datetime import datetime

import logging


class JSONHashTableDB:
    def __init__(self):
        self.records = {}  # Hash table (dict)
        self.log = logging.getLogger("JSONHashTableDB")
        self.log.debug("Hello From JSONHashTableDB")

    def add(self, key, value):
        """Add or update a record by key."""
        self.records[key] = value
    

    def delete(self, key):
        """Delete a record by key."""
        if key in self.records:
            del self.records[key]
        else:
            print(f"Key '{key}' not found.")

    def clear_all(self):
        """Clear all records."""
        print("Clearing records...")
        self.log.debug("Clearing records...")
        self.records.clear()
        self.log.debug("After clear:", self.records)
        print("After clear:", self.records)
        
    
    def read_one(self, key):
        """Read a single record by key."""
        return self.records.get(key, f"Key '{key}' not found.")

    def read_all(self):
        """Return all records."""
        return self.records

    def count(self):
        """Return the number of records."""
        return len(self.records)

# Example usage
# if __name__ == "__main__":
#     db = JSONHashTableDB("records.json")

#     db.add("u1", {"name": "Alice", "role": "Admin"})
#     db.add("u2", {"name": "Bob", "role": "User"})

#     print("Read one:", db.read_one("u1"))
#     print("All records:", db.read_all())
#     print("Count:", db.count())

#     db.delete("u1")
#     print("After deletion:", db.read_all())

#     db.clear_all()
#     print("After clearing:", db.read_all())
#     print("Count:", db.count())

class VoterTally:
    def __init__(self):
        self.records = {}  # Hash table (dict)
        self.log = logging.getLogger("VoterTally")
        self.log.debug("Hello From Below")

    def add(self, key, value):
        """Add or update a record by key."""
        self.records[key] = value
    

    def delete(self, key):
        """Delete a record by key."""
        if key in self.records:
            del self.records[key]
        else:
            print(f"Key '{key}' not found.")

    def clear_all(self):
        """Clear all records."""
        print("Clearing records...")
        self.log.debug("Clearing records...")
        self.records.clear()
        #self.log.debug("After clear:" + str(self.records))
        #print("After clear:", str(self.records))
        
    
    def read_one(self, key):
        """Read a single record by key."""
        return self.records.get(key, f"Key '{key}' not found.")

    def read_all(self):
        """Return all records."""
        return self.records

    def count(self):
        """Return the number of records."""
        return len(self.records)



class Watchdog:
    def __init__(self):
        self.timer = None  # Safely initialize the timer
        pass

    def start(self, timeout, callback):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.timer = threading.Timer(timeout, callback)
        self.timer.start()

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None


def timeout_callback():
    print("Watchdog timeout! Resetting or taking action...")
    # Add your reset or recovery logic here

# if __name__ == "__main__":
#     watchdog = Watchdog(5, timeout_callback)  # Set a 5-second timeout
#     watchdog.start()

#     try:
#         while True:
#             print("Doing some work...")
#             time.sleep(2)  # Simulate work being done
#             watchdog.reset()  # Reset the watchdog timer
#     except KeyboardInterrupt:
#         watchdog.stop()
#         print("Program stopped.")

class ConvertDateTime:
    def __init__(self):
        self.log = logging.getLogger("ConvertDateTime")
        self.log.debug("Initializing ConvertDateTime...")

    def has_offset(self, dt_str):
        return 'Z' in dt_str or '+' in dt_str or '-' in dt_str[10:]  # skip date part for '-'

    def replace_tz_with_offset(self, datetime_str):
        # Match timezone at end (e.g., "2025-05-02 10:30:00 EST")
        tz_map = {
            'UTC': '+0000',
            'EST': '-0500',
            'EDT': '-0400',
            'CST': '-0600',
            'CDT': '-0500',
            'MST': '-0700',
            'MDT': '-0600',
            'PST': '-0800',
            'PDT': '-0700'
        }
        match = re.search(r'\s([A-Z]{2,4})$', datetime_str)
        if match:
            tz_abbr = match.group(1)
            offset = tz_map.get(tz_abbr)
            if offset:
                # Replace timezone abbreviation with offset
                return datetime_str.replace(f" {tz_abbr}", offset)
        return datetime_str  # Return unchanged if no match
    
    def normalize_offset(self, dt_str):
        
        self.replace_tz_with_offset(dt_str)
        # Handle 'Z' UTC suffix
        if dt_str.endswith('Z'):
            return dt_str[:-1] + '+00:00'

        # Handle offsets like -0400 or +0530 (no colon)
        match = re.search(r'([+-])(\d{2})(\d{2})$', dt_str)
        if match:
            sign, hour, minute = match.groups()
            return dt_str[:-5] + f'{sign}{hour}:{minute}'

        # If already in ±HH:MM or no offset, return as-is
        return dt_str

    def convert(self, datetimestring):
        self.datetime_str = datetimestring
       
        date_formats = [
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%dT%H:%M:%S%Z",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S%Z",
                    "%m/%d/%Y %H:%M:%S",
                    "%m/%d/%Y %H:%M",
                    "%m/%d/%Y %H",
                    "%Y/%m/%d %H:%M:%S",
                    "%Y/%m/%d %H:%M",
                    "%Y-%m-%d %H:%M:$S",
                    "%Y-%m-%d %H:%M"
        ]
        #2025-04-23T19:00:00-04:00
        #datetime_str = self.datetime_str.replace('Z', '+00:00') if self.has_offset(self.datetime_str) else self.datetime_str
        datetime_str = self.normalize_offset(self.datetime_str)
        for fmt in date_formats:
            try:
                dt1 = datetime.strptime(datetime_str, fmt)
                dt_naive = dt1.replace(tzinfo=None)
                self.log.debug(f"ConvertDateTime: Parsed successfully: {dt_naive} (format: {fmt})")
                print(dt_naive)
                return dt_naive
            except ValueError:
                continue
        else:
            print("ConvertDateTime: No matching format found." + self.datetime_str)
            self.log.debug("ConvertDateTime: No matching format found." + self.datetime_str)

        return dt1