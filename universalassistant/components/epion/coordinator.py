"""The Epion data coordinator."""

import logging
from typing import Any, override

from epion import Epion, EpionAuthenticationError, EpionConnectionError

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import REFRESH_INTERVAL

_LOGGER = logging.getLogger(__name__)

type EpionConfigEntry = ConfigEntry[EpionCoordinator]


class EpionCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Epion data update coordinator."""

    def __init__(
        self, hass: __HAC_KEEP__, entry: EpionConfigEntry, epion_api: Epion
    ) -> None:
        """Initialize the Epion coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name="Epion",
            update_interval=REFRESH_INTERVAL,
        )
        self.epion_api = epion_api

    @override
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Epion API, construct a dict with device IDs as keys."""
        try:
            response = await self.hass.async_add_executor_job(
                self.epion_api.get_current
            )
        except EpionAuthenticationError as err:
            raise ConfigEntryAuthFailed("Authentication error with Epion API") from err
        except EpionConnectionError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        device_data = {}
        for epion_device in response["devices"]:
            device_data[epion_device["deviceId"]] = epion_device
        return device_data
