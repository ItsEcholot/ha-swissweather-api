""" Setup integration """
import logging
import asyncio
from homeassistant.core import Config, HomeAssistant
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from .const import (
    CONF_ZIP_CODE,
    DOMAIN,
    CONF_API_KEY,
    CONF_SIG_SALT,
    HASS_DATA_CLIENT,
    ENTITY_WEATHER_NAME,
)
from .swiss_weather_api_client import SwissWeatherAPIClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Setup integration."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, config: Config):
    """Setup a config entry."""
    hass.data.setdefault(DOMAIN, {})

    client = await hass.async_add_executor_job(
        SwissWeatherAPIClient,
        config.data[CONF_ZIP_CODE],
        config.data[CONF_API_KEY],
        config.data[CONF_SIG_SALT],
    )
    _LOGGER.debug("Current configuration: %s", config.data)

    hass.data[DOMAIN][HASS_DATA_CLIENT] = client
    await hass.async_add_executor_job(hass.data[DOMAIN][HASS_DATA_CLIENT].update)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config, ENTITY_WEATHER_NAME)
    )
    _LOGGER.debug("Start weather entity")
    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(
                    entry, ENTITY_WEATHER_NAME
                )
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.data)

    return True
