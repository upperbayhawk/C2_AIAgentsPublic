# ==============================================================================
# Module: weatherlib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library for accessing National Weather Service forecast data for a location
# Notes: https://github.com/spectrshiv/python-weather_gov
# 
# ==============================================================================
import nwsweatherlib
import logbook

class XWeather:
    def __init__(self):
        #public weather from National Weather Service
       
        self.log = logbook.Logger("Weather")
        self.log.debug("Hello From Below")

    def get_weather_data(self):
        try:

            # Most data must be retrieved via gridpoints, which are derived from LAT/LON.
            # West Longitude is negative!
            # This is "Lewes" in Delaware
            LAT = 39.7810
            LON = -75.1571
            
            # Get forecast for the specified latitude and longitude
            nws = nwsweatherlib.NWSWeather()
            #forecast = nws.get_forecast(LAT, LON)
            forecast = nws.get_temperature_forecast(LAT, LON)
            print(forecast)     
            # Print detailed forecast information
            for period in forecast['properties']['periods']:
                start_time = period['startTime']
                temperature = period['temperature']
                temperature_unit = period['temperatureUnit']
                short_forecast = period['shortForecast']
                print(f"{start_time}: {temperature} {temperature_unit}\nForecast: {short_forecast}\n")

            # Open the file in write mode
            with open('data/PumpDataPrompt.json', 'w') as file:
                for period in forecast['properties']['periods']:
                    start_time = period['startTime']
                    temperature = period['temperature']
                    temperature_unit = period['temperatureUnit']
                    short_forecast = period['shortForecast']
                    file.write(f"{start_time},{temperature},{short_forecast}\n")
                   
        except Exception as ex:
            self.log.error("Exception " + str(ex))
            print ("Exception " + str(ex))
        return "OK"