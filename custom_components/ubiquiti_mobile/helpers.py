"""Helper utilities for the Ubiquiti Mobile integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv

from .const import CONF_ENABLE_CLIENT_TRACKERS, DEFAULT_ENABLE_CLIENT_TRACKERS


def is_client_tracker_enabled(config_entry: ConfigEntry) -> bool:
    """Return True if client device trackers should be created."""
    raw_value: Any | None = config_entry.options.get(CONF_ENABLE_CLIENT_TRACKERS)
    if raw_value is None:
        return DEFAULT_ENABLE_CLIENT_TRACKERS

    if isinstance(raw_value, bool):
        return raw_value

    try:
        return cv.boolean(raw_value)
    except vol.Invalid:
        return DEFAULT_ENABLE_CLIENT_TRACKERS
