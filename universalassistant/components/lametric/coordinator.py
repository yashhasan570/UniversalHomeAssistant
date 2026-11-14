"""DataUpdateCoordinator for the LaMatric integration."""

from typing import override

from demetriek import Device, LaMetricAuthenticationError, LaMetricDevice, LaMetricError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_API_KEY, CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type LaMetricConfigEntry = ConfigEntry[LaMetricDataUpdateCoordinator]


class LaMetricDataUpdateCoordinator(DataUpdateCoordinator[Device]):
    """The LaMetric Data Update Coordinator."""

    config_entry: LaMetricConfigEntry

    def __init__(self, hass: __HAC_KEEP__, entry: LaMetricConfigEntry) -> None:
        """Initialize the LaMatric coordinator."""
        self.lametric = LaMetricDevice(
            host=entry.data[CONF_HOST],
            api_key=entry.data[CONF_API_KEY],
            session=async_get_clientsession(hass),
        )

        super().__init__(
            hass, LOGGER, config_entry=entry, name=DOMAIN, update_interval=SCAN_INTERVAL
        )

    @override
    async def _async_update_data(self) -> Device:
        """Fetch device information of the LaMetric device."""
        try:
            return await self.lametric.device()
        except LaMetricAuthenticationError as err:
            raise ConfigEntryAuthFailed from err
        except LaMetricError as ex:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
                translation_placeholders={"error": str(ex)},
            ) from ex
