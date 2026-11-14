"""Automation manager for boards manufactured by ProgettiHWSW Italy."""

from ProgettiHWSW.input import Input
from ProgettiHWSW.ProgettiHWSWAPI import ProgettiHWSWAPI
from ProgettiHWSW.relay import Relay

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SWITCH]

type ProgettiHWSWConfigEntry = ConfigEntry[ProgettiHWSWAPI]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: ProgettiHWSWConfigEntry
) -> None:
    """Set up ProgettiHWSW Automation from a config entry."""
    api = ProgettiHWSWAPI(f"{entry.data['host']}:{entry.data['port']}")

    # Check board validation again to load new values to API.
    await api.check_board()

    entry.runtime_data = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: ProgettiHWSWConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


def setup_input(api: ProgettiHWSWAPI, input_number: int) -> Input:
    """Initialize the input pin."""
    return api.get_input(input_number)


def setup_switch(api: ProgettiHWSWAPI, switch_number: int, mode: str) -> Relay:
    """Initialize the output pin."""
    return api.get_relay(switch_number, mode)
