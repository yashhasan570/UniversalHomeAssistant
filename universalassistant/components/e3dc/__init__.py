"""Integrate E3/DC home power stations into __HA_KEEP__."""

from e3dc_ess_modbus import E3dcPowerStation

from universalassistant.components.modbus import async_get_unit
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError, __HAC_KEEP__Error

from .config_flow import create_modbus_params
from .const import DOMAIN, UNIT_ID
from .coordinator import E3dcConfigEntry, E3dcDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: E3dcConfigEntry) -> None:
    """Set up E3/DC from a config entry."""
    try:
        unit = async_get_unit(hass, entry, create_modbus_params(entry.data), UNIT_ID)
    except __HAC_KEEP__Error as err:
        raise ConfigEntryError(
            translation_domain=err.translation_domain,
            translation_key=err.translation_key,
            translation_placeholders=err.translation_placeholders,
        ) from err
    device = E3dcPowerStation(unit)
    entry.async_on_unload(device.close)

    coordinator = E3dcDataUpdateCoordinator(hass, entry, device)
    # The first poll also reads the identity and probes which blocks the station serves
    await coordinator.async_config_entry_first_refresh()
    if device.serial_number != entry.unique_id:
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="serial_mismatch",
            translation_placeholders={
                "expected": str(entry.unique_id),
                "found": str(device.serial_number),
            },
        )

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: E3dcConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
