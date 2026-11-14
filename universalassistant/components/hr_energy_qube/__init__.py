"""The Qube Heat Pump integration."""

from modbus_connection import ModbusTcpParams
from python_qube_heatpump import QubeClient

from universalassistant.components.modbus import async_get_unit
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_PORT
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError, UniversalAssistantError

from .const import DOMAIN, PLATFORMS, UNIT_ID
from .coordinator import QubeCoordinator

type QubeConfigEntry = ConfigEntry[QubeCoordinator]


async def async_setup_entry(hass: UniversalAssistant, entry: QubeConfigEntry) -> None:
    """Set up Qube Heat Pump from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    try:
        # Borrowed from the modbus integration, which shares one connection
        # per device and closes it when the last entry using it unloads
        unit = async_get_unit(
            hass, entry, ModbusTcpParams(host=host, port=port), UNIT_ID
        )
    except UniversalAssistantError as err:
        # The device is already in use over different link settings
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="link_settings_in_use",
            translation_placeholders={"error": str(err)},
        ) from err

    client = QubeClient(host, port, UNIT_ID, unit=unit)
    coordinator = QubeCoordinator(hass, client, entry)

    entry.runtime_data = coordinator

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: QubeConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
