# ==============================================================================
# Module: thingspeaklib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library for accessing thingspeak.com
# Notes: https://thingspeak.readthedocs.io/en/latest/
# ==============================================================================

import thingspeak
import logbook

class XThingspeak:
    def __init__(self):
        #public weather station at Matlab
        self.channel_key = 'U'
        self.channel_id = 12397
        self.field = 4
        self.num_of_values = 10
        
        self.log = logbook.Logger("Thingspeak")
        self.log.debug("Hello From Below")

    def get_thingspeak_data(self):
        ch = thingspeak.Channel(self.channel_id,api_key=self.channel_key)
        #get allfields in channel
        #my_results = ch.get(options={'results': 10,'minutes':60})
        #get one field in channel
        #NOTE: 600 results blows up openai limit of 32K in prompt
        my_results = ch.get_field(field=self.field,options={'results': self.num_of_values})
        print(my_results)
        # Open the file in write mode
        with open('data/PumpDataPrompt.json', 'w') as file:
            file.write(my_results)
        self.log.debug("get_thingspeak_data: " + str(self.channel_id))
        return "OK"