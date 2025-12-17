"""Adds config flow for Blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.ubiquiti_mobile.data import SessionData

from .api import UbiquitiMobileApiClient
from .const import (
    CONF_ENABLE_CLIENT_TRACKERS,
    DEFAULT_ENABLE_CLIENT_TRACKERS,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigFlowResult


class UbiquitiMobileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ubiquiti Mobile Gateway."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the configuration flow that is presented to the user."""
        errors = {}

        # If user input is defined, then the form has been submitted
        if user_input:
            host = user_input["host"].rstrip("/")
            username = user_input["username"]
            password = user_input["password"]

            session_data = SessionData(host=host, username=username, password=password)
            aiohttp_session = async_get_clientsession(self.hass)
            client = UbiquitiMobileApiClient(session_data, aiohttp_session)

            # attempt login and fetch status
            await client.async_start_session()
            status = await client.get_device_info()

            if status.result is not None:
                return self.async_create_entry(
                    title="Ubiquiti Mobile " + status.result.mac or host,
                    description=status.result.model_name,
                    # This is all of the data that is required to re-create this entry
                    # whenhome assistant restarts. vars() converts the dataobject to a
                    # dictionary, which is how the data will be presented to this
                    # configuration when home assistant restarts. Converting it keeps
                    # the locic in __init__ the same regardless.
                    data={"session_data": vars(session_data)},
                )

        data_schema = vol.Schema(
            {
                vol.Required(
                    "host",
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
                ),
                vol.Required("username", default="ui"): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
                ),
                vol.Required("password"): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.PASSWORD
                    ),
                ),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow handler."""
        return UbiquitiMobileOptionsFlowHandler(config_entry)


class UbiquitiMobileOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Ubiquiti Mobile Gateway options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_ENABLE_CLIENT_TRACKERS,
                    default=self.config_entry.options.get(
                        CONF_ENABLE_CLIENT_TRACKERS,
                        DEFAULT_ENABLE_CLIENT_TRACKERS,
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
