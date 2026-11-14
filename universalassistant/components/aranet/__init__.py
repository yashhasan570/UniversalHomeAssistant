"""The Aranet integration."""

import logging

from aranet4.client import Aranet4Advertisement

from universalassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
from universalassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type AranetConfigEntry = ConfigEntry[
    PassiveBluetoothProcessorCoordinator[Aranet4Advertisement]
]


def _service_info_to_adv(
    service_info: BluetoothServiceInfoBleak,
) -> Aranet4Advertisement:
    return Aranet4Advertisement(service_info.device, service_info.advertisement)


async def async_setup_entry(hass: __HAC_KEEP__, entry: AranetConfigEntry) -> None:
    """Set up Aranet from a config entry."""

    address = entry.unique_id
    assert address is not None
    coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=_service_info_to_adv,
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())


async def async_unload_entry(hass: __HAC_KEEP__, entry: AranetConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
