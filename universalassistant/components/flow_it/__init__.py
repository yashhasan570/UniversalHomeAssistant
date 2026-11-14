"""The AriaQ integration."""

import logging

from flow_it_api.client import FlowItVMCMachine

from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.httpx_client import get_async_client

from .coordinator import AriaQConfigEntry, AriaQCoordinator, AriaQData

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.FAN,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: UniversalAssistant, entry: AriaQConfigEntry) -> None:
    """Set up AriaQ from a config entry."""

    vmc = FlowItVMCMachine(
        entry.data[CONF_HOST],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_USERNAME],
        session=get_async_client(hass),
    )

    coordinator = AriaQCoordinator(hass, entry, vmc)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = AriaQData(
        vmc=vmc,
        coordinator=coordinator,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AriaQConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    vmc = entry.runtime_data.vmc
    await vmc.close()
