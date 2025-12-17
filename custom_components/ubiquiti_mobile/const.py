"""Constants for ubiquiti_mobile."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ubiquiti_mobile"

CONF_HOST = "host"
CONF_ENABLE_CLIENT_TRACKERS = "enable_client_trackers"

DEFAULT_ENABLE_CLIENT_TRACKERS = True

PLATFORMS: list[str] = ["sensor", "device_tracker"]
