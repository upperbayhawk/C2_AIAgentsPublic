import requests

class NWSWeather:
    def __init__(self):
        self.base_url = "https://api.weather.gov"
        self.headers = {'User-Agent': 'MyApp (dave@upperbay.com)'}

    def get_nws_data(self, lat, lon):
        """
        Retrieve forecast data from NWS API for a given latitude and longitude.
        """
        #endpoint = f"{self.base_url}/points/{lat},{lon}/forecast"
        endpoint = f"{self.base_url}/points/{lat},{lon}"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()  # Will raise an exception for HTTP errors
            return response.json()
        except requests.HTTPError as e:
            return {'error': f'HTTP Error: {e.response.status_code} - {e.response.reason}'}        
        except requests.RequestException as e:
            return {'error': str(e)}

    def get_nws_hourly_forecast(self, url):
        """
        Retrieve forecast data from NWS API for a given latitude and longitude.
        """
        endpoint = url
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()  # Will raise an exception for HTTP errors
            return response.json()
        except requests.HTTPError as e:
            return {'error': f'HTTP Error: {e.response.status_code} - {e.response.reason}'}        
        except requests.RequestException as e:
            return {'error': str(e)}

    def get_temperature_forecast(self, lat, lon):
        """
        Extract temperature forecasts from the forecast data.
        """
        nws_data = self.get_nws_data(lat, lon)
        if 'error' in nws_data:
            return nws_data  # Return error if request failed

        #periods = forecast_data.get('properties', {}).get('periods', [])
        forecast_url = nws_data.get('properties', {}).get('forecastHourly',{})
        print("Forecast URL = " + forecast_url)
        nws_fourcast = self.get_nws_hourly_forecast(forecast_url)
        print(nws_fourcast)

        """ temperature_forecast = [{
            'time': period['name'],
            'temperature': period['temperature'],
            'unit': period['temperatureUnit'],
            'detailedForecast': period['detailedForecast']
        } for period in periods] """
        return nws_fourcast

# Usage example function
def fetch_temperature_forecast(lat, lon):
    nws = NWSWeather()
    forecast = nws.get_temperature_forecast(lat, lon)
    return forecast
