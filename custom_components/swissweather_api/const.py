""" Defines constants used throughout the integration. """

DOMAIN = "swissweather_api"
CONF_ZIP_CODE = "zip_code"
CONF_API_KEY = "api_key"
CONF_SIG_SALT = "sig_salt"
HASS_DATA_CLIENT = "client"
ENTITY_WEATHER_NAME = "weather"

WEATHER_DATA_CUR_WEATHER = "current_weather"
WEATHER_DATA_FORECAST_WEATHER = "forecast"
WEATHER_DATA_AIR_QUALITY = "air_quality"
WEATHER_DATA_AIR_QUALITY_OZONE = "ozone"
WEATHER_DATA_SYMBOL = "symbol"
WEATHER_DATA_TEMPERATURE = "temperature"
WEATHER_DATA_PRESSURE = "pressure_hpa"
WEATHER_DATA_HUMIDITY = "humidity"
WEATHER_DATA_WIND_SPEED = "wind_speed"
WEATHER_DATA_WIND_BEARING = "wind_direction"
WEATHER_FORECAST_TIMESTAMP = "timestamp"
WEATHER_FORECAST_PRECIPITATION = "precipitation_amount"
WEATHER_FORECAST_PRECIPITATION_PROBABILITY = "precipitation_probability"
WEATHER_DATA_SYMBOL_CONDITION_MAP = {
    "clear-night": ["night_clear"],
    "cloudy": [
        "heavy_clouds",
        "some_clouds",
        "night_heavy_clouds",
        "night_some_clouds",
    ],
    "exceptional": [],
    "fog": ["light_fog", "fog", "night_light_fog", "night_fog"],
    "hail": [],
    "lightning": [
        "partly_sunny_dry_thunderstorms",
        "night_partly_cloudy_dry_thunderstorms",
    ],
    "lightning-rainy": [
        "overcast_thunderstorms",
        "heavy_clouds_light_thunderstorms",
        "heavy_clouds_some_thunderstorms",
        "heavy_clouds_heavy_thunderstorms",
        "partly_sunny_some_rain_showers",
        "night_overcast_thunderstorms",
        "night_heavy_clouds_light_thunderstorms",
        "night_heavy_clouds_some_thunderstorms",
        "night_heavy_clouds_heavy_thunderstorms",
        "night_partly_cloudy_some_rain_showers",
    ],
    "partlycloudy": [
        "mostly_sunny_light_clouds",
        "partly_sunny_some_clouds",
        "overcast",
        "night_light_clouds",
        "night_partly_cloudy",
        "night_overcast",
    ],
    "pouring": ["heavy_clouds_heavy_rain", "night_heavy_clouds_heavy_rain"],
    "rainy": [
        "overcast_light_rain_showers",
        "overcast_some_rain_showers",
        "heavy_clouds_light_rain",
        "heavy_clouds_some_rain",
        "partly_sunny_light_rain_showers",
        "overcast_heavy_rain",
        "night_overcast_light_rain_showers",
        "night_overcast_some_rain_showers",
        "night_heavy_clouds_light_rain",
        "night_heavy_clouds_some_rain",
        "night_partly_cloudy_light_rain_showers",
        "night_overcast_heavy_rain",
    ],
    "snowy": [
        "overcast_light_snow_showers",
        "overcast_some_snow_showers",
        "heavy_clouds_light_snow",
        "heavy_clouds_some_snow",
        "heavy_clouds_heavy_snow",
        "partly_sunny_light_snow_showers",
        "overcast_heavy_snow",
        "night_overcast_light_snow_showers",
        "night_overcast_some_snow_showers",
        "night_heavy_clouds_light_snow",
        "night_heavy_clouds_some_snow",
        "night_heavy_clouds_heavy_snow",
        "night_partly_cloudy_light_snow_showers",
        "night_overcast_heavy_snow",
    ],
    "snowy-rainy": [
        "overcast_light_sleet_showers",
        "overcast_some_sleet_showers",
        "heavy_clouds_light_sleet",
        "heavy_clouds_some_sleet",
        "heavy_clouds_heavy_sleet",
        "partly_sunny_light_sleet_showers",
        "night_overcast_light_sleet_showers",
        "night_overcast_some_sleet_showers",
        "night_heavy_clouds_light_sleet",
        "night_heavy_clouds_some_sleet",
        "night_heavy_clouds_heavy_sleet",
        "night_partly_cloudy_light_sleet_showers",
    ],
    "sunny": ["sunny", "high_cloud_fields", "night_high_cloud_fields"],
    "windy": [],
    "windy-variant": [],
}
