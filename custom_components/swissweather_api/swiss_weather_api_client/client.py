"""Defines the SwissWeather API client."""
import logging
import time
import hashlib
import requests

SWA_BASE_URL = "https://weather.echolot.io"
SWA_ZIP_CODE_WEATHER_BASE_PATH = "/location/zip"
SWA_LOCATION_SEARCH_LAT_LON = "/location/search/cords"


class SwissWeatherAPIClient:
    """Implements the SwissWeather API client."""

    def __init__(self, zip_code=None, api_key=None, sig_salt=None):
        self._zip_code = zip_code
        self._api_key = api_key
        self._sig_salt = sig_salt
        self._weather_data = None
        self._weather_data_etag = None

    def __prepare_request_url(self, request_path):
        """Generate and return a request url."""
        curr_timestamp = int(time.time() * 1000)
        request_str = (
            f"{request_path}?api_key={self._api_key}&curr_timestamp={curr_timestamp}"
        )
        sig = hashlib.md5(
            f"{request_str}&sig_salt={self._sig_salt}".encode()
        ).hexdigest()
        return f"{SWA_BASE_URL}{request_str}&sig={sig}"

    def fetch_weather_data(self):
        """Fetch the raw weather data from the api."""
        request = requests.get(
            self.__prepare_request_url(
                f"{SWA_ZIP_CODE_WEATHER_BASE_PATH}/{self._zip_code}"
            ),
            headers={"If-None-Match": self._weather_data_etag},
        )
        if (
            request.status_code == 503
            and request.headers.get("retry-after") is not None
        ):
            time.sleep(int(request.headers.get("retry-after")))
            self.fetch_weather_data()
        else:
            request.raise_for_status()
            if request.status_code != 304:
                self._weather_data = request.json()
                self._weather_data_etag = request.headers.get("ETag")

    def update(self):
        """Update the weather data stored in the instance."""
        self.fetch_weather_data()

    def is_credentials_valid(self):
        """Check if api credentials are valid by making a request."""
        try:
            # Use location query for Aarau to check if credentials are valid.
            if self.get_zip_code_by_lat_lon(47.391117, 8.048300) == 5000:
                return True
            return False
        except requests.HTTPError:
            return False

    def get_zip_code_by_lat_lon(self, lat, lon):
        """Fetch and return zip code from coordinates (lat/lon)."""
        request = requests.get(
            self.__prepare_request_url(f"{SWA_LOCATION_SEARCH_LAT_LON}/{lat}/{lon}")
        )
        request.raise_for_status()
        return request.json().get("plz")

    def get_weather_data(self):
        """Returns fetched weather data from memory."""
        return self._weather_data
