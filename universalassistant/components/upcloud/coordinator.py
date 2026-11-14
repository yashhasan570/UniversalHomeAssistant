"""Coordinator for UpCloud."""

import logging
from typing import override

import upcloud_api

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


type UpCloudConfigEntry = ConfigEntry[UpCloudDataUpdateCoordinator]


class UpCloudDataUpdateCoordinator(
    DataUpdateCoordinator[dict[str, upcloud_api.Server]]
):
    """UpCloud data update coordinator."""

    def __init__(
        self,
        hass: __HAC_KEEP__,
        *,
        config_entry: UpCloudConfigEntry,
        cloud_manager: upcloud_api.CloudManager,
        username: str,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=f"{username}@UpCloud",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.cloud_manager = cloud_manager

    @override
    async def _async_update_data(self) -> dict[str, upcloud_api.Server]:
        return {
            x.uuid: x
            for x in await self.hass.async_add_executor_job(
                self.cloud_manager.get_servers
            )
        }
