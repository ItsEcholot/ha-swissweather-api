"""Config flow to configure the SwissWeather API integration."""
import logging
import re
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import CONF_API_KEY, CONF_SIG_SALT, DOMAIN, CONF_ZIP_CODE
from .swiss_weather_api_client import SwissWeatherAPIClient

_LOGGER = logging.getLogger(__name__)


class SwissWeatherAPIFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handles SwissWeather API Configuration Flow."""

    def __init__(self):
        """Init FlowHandler."""
        self._errors = {}

    async def validate_config(self, config):
        """Validate user config."""

        # check valid api_key and sig_salt
        client: SwissWeatherAPIClient = await self.hass.async_add_executor_job(
            SwissWeatherAPIClient,
            config[CONF_ZIP_CODE],
            config[CONF_API_KEY],
            config[CONF_SIG_SALT],
        )

        valid = await self.hass.async_add_executor_job(client.is_credentials_valid)
        if not valid:
            self._errors[CONF_API_KEY] = "invalid_api_key_or_sig_salt"
            _LOGGER.warning("API key or Signature Salt is invalid")

        # check valid zip-code
        if not re.match(r"^\d{4}$", str(config[CONF_ZIP_CODE])):
            self._errors[CONF_ZIP_CODE] = "invalid_zip_code"
            _LOGGER.warning("%s is not a valid zip code", config[CONF_ZIP_CODE])

        if len(self._errors) == 0:
            _LOGGER.info("Configuration for meteo swiss integration validated")
            return True

        _LOGGER.error("Configuration error for meteo suisse integration")
        return False

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        self._errors = {}
        if user_input is not None:
            if await self.validate_config(user_input):
                return self.async_create_entry(
                    title=user_input[CONF_ZIP_CODE], data=user_input
                )
            return self._show_config_form(user_input)

        return self._show_config_form(user_input)

    @callback
    def _show_config_form(self, user_input):
        """Show the setup form to the user."""

        if user_input is None:
            user_input = {}

        data_schema = {
            vol.Required(CONF_ZIP_CODE): int,
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_SIG_SALT): str,
        }

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def async_step_import(self, user_input):
        """Import a config entry."""
        return await self.async_step_user(user_input)
