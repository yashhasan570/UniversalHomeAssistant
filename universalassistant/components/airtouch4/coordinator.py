"""DataUpdateCoordinator for the airtouch integration."""

from datetime import timedelta
import logging
from typing import Any, override

from airtouch4pyapi import AirTouch
from airtouch4pyapi.airtouch import AirTouchStatus

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)

type AirTouch4ConfigEntry = ConfigEntry[AirtouchDataUpdateCoordinator]


class AirtouchDataUpdateCoordinator(
    DataUpdateCoordinator[dict[str, list[dict[str, Any]]]]
):
    """Class to manage fetching Airtouch data."""

    def __init__(
        self, hass: __HAC_KEEP__, entry: AirTouch4ConfigEntry, airtouch: AirTouch
    ) -> None:
        """Initialize global Airtouch data updater."""
        self.airtouch = airtouch

        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    @override
    async def _async_update_data(self) -> dict[str, list[dict[str, Any]]]:
        """Fetch data from Airtouch."""
        await self.airtouch.UpdateInfo()
        if self.airtouch.Status != AirTouchStatus.OK:
            raise UpdateFailed("Airtouch connection issue")
        return {
            "acs": [
                {"ac_number": ac.AcNumber, "is_on": ac.IsOn}
                for ac in self.airtouch.GetAcs()
            ],
            "groups": [
                {
                    "group_number": group.GroupNumber,
                    "group_name": group.GroupName,
                    "is_on": group.IsOn,
                }
                for group in self.airtouch.GetGroups()
            ],
        }
