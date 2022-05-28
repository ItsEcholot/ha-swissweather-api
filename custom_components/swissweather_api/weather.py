"""Defines the weather component entity."""

import logging
import datetime, pytz
from homeassistant.components.weather import Forecast, WeatherEntity
from .swiss_weather_api_client import SwissWeatherAPIClient
from .const import (
    CONF_ZIP_CODE,
    DOMAIN,
    HASS_DATA_CLIENT,
    WEATHER_DATA_AIR_QUALITY,
    WEATHER_DATA_AIR_QUALITY_OZONE,
    WEATHER_DATA_CUR_WEATHER,
    WEATHER_DATA_FORECAST_WEATHER,
    WEATHER_DATA_HUMIDITY,
    WEATHER_DATA_PRESSURE,
    WEATHER_DATA_SYMBOL,
    WEATHER_DATA_SYMBOL_CONDITION_MAP,
    WEATHER_DATA_TEMPERATURE,
    WEATHER_DATA_WIND_BEARING,
    WEATHER_DATA_WIND_SPEED,
    WEATHER_FORECAST_PRECIPITATION,
    WEATHER_FORECAST_PRECIPITATION_PROBABILITY,
    WEATHER_FORECAST_TIMESTAMP,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_entities):
    client = hass.data[DOMAIN][HASS_DATA_CLIENT]
    timezone = hass.config.time_zone
    zip = config.data[CONF_ZIP_CODE]
    async_add_entities([SwissWeatherAPIWeather(client, zip, timezone)], True)


class SwissWeatherAPIWeather(WeatherEntity):
    """Implements weather entity."""

    def __init__(self, client: SwissWeatherAPIClient, plz: int, timezone: str):
        self._client = client
        self._display_name = f"SwissWeatherAPI - {plz}"
        self._weather_data = None
        self._timezone = timezone

    def update(self):
        """Update Condition and Forecast."""
        self._client.update()
        self._weather_data = self._client.get_weather_data()

    @property
    def name(self):
        return self._display_name

    @property
    def condition(self):
        symbol_str = self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_SYMBOL
        )
        condition = next(
            (
                k
                for k, v in WEATHER_DATA_SYMBOL_CONDITION_MAP.items()
                if symbol_str in v
            ),
            None,
        )
        return condition

    @property
    def temperature(self):
        return self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_TEMPERATURE
        )

    @property
    def temperature_unit(self) -> str:
        return "°C"

    @property
    def pressure(self) -> float:
        return self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_PRESSURE
        )

    @property
    def pressure_unit(self) -> str:
        return "hPa"

    @property
    def humidity(self) -> float:
        return self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_HUMIDITY
        )

    @property
    def ozone(self) -> float:
        return (
            self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {})
            .get(WEATHER_DATA_AIR_QUALITY, {})
            .get(WEATHER_DATA_AIR_QUALITY_OZONE)
        )

    @property
    def wind_speed(self) -> float:
        return self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_WIND_SPEED
        )

    @property
    def wind_speed_unit(self) -> str:
        return "km/h"

    @property
    def wind_bearing(self) -> float:
        return self._weather_data.get(WEATHER_DATA_CUR_WEATHER, {}).get(
            WEATHER_DATA_WIND_BEARING
        )

    @property
    def forecast(self) -> list[Forecast]:
        return map(
            self.create_forecast_entry,
            self._weather_data.get(WEATHER_DATA_FORECAST_WEATHER, [])[1:],
        )

    def create_forecast_entry(self, entry):
        """Converts the SwissWeatherAPI Forecast entry to the HomeAssistant format"""
        out_entry = {}
        out_entry["datetime"] = pytz.utc.localize(
            datetime.datetime.utcfromtimestamp(
                entry.get(WEATHER_FORECAST_TIMESTAMP, 0) / 1000
            )
        ).isoformat()
        out_entry["temperature"] = entry.get(WEATHER_DATA_TEMPERATURE)
        out_entry["condition"] = next(
            (
                k
                for k, v in WEATHER_DATA_SYMBOL_CONDITION_MAP.items()
                if entry.get(WEATHER_DATA_SYMBOL) in v
            ),
            None,
        )
        out_entry["precipitation"] = entry.get(WEATHER_FORECAST_PRECIPITATION)
        out_entry["precipitation_probability"] = entry.get(
            WEATHER_FORECAST_PRECIPITATION_PROBABILITY
        )
        out_entry["pressure"] = entry.get(WEATHER_DATA_PRESSURE)
        out_entry["wind_bearing"] = entry.get(WEATHER_DATA_WIND_BEARING)
        out_entry["wind_speed"] = entry.get(WEATHER_DATA_WIND_SPEED)
        return out_entry
