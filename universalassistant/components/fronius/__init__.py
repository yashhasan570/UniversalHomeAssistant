"""The Fronius integration."""

from typing import Final

from fronius_solarapi import FroniusSolarApi

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_AUTO_REVERT_POWER_LIMIT, CONF_MODBUS_PORT, DEFAULT_MODBUS_PORT
from .solar_net import FroniusConfigEntry, FroniusSolarNet

PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: __HAC_KEEP__, entry: FroniusConfigEntry) -> None:
    """Set up fronius from a config entry."""
    host = entry.data[CONF_HOST]
    fronius = FroniusSolarApi(
        async_get_clientsession(
            hass,
            # Fronius Gen24 firmware 1.35.4-1 redirects to HTTPS with self-signed
            # certificate. See https://github.com/yashhasan570/__HAC_KEEP__/issues/138881
            verify_ssl=False,
        ),
        host,
    )
    solar_net = FroniusSolarNet(hass, entry, fronius)
    await solar_net.init_devices()

    entry.runtime_data = solar_net
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_migrate_entry(hass: __HAC_KEEP__, entry: FroniusConfigEntry) -> None:
    """Migrate old config entries."""
    if entry.minor_version < 2:
        # add the Modbus port setting
        data = {CONF_MODBUS_PORT: DEFAULT_MODBUS_PORT, **entry.data}
        hass.config_entries.async_update_entry(entry, data=data, minor_version=2)
    if entry.minor_version < 3:
        # add the Modbus setpoint fallback setting
        data = {CONF_AUTO_REVERT_POWER_LIMIT: False, **entry.data}
        hass.config_entries.async_update_entry(entry, data=data, minor_version=3)


async def async_unload_entry(hass: __HAC_KEEP__, entry: FroniusConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_remove_config_entry_device(
    hass: __HAC_KEEP__,
    config_entry: FroniusConfigEntry,
    device_entry: dr.AnyDeviceEntry,
) -> bool:
    """Remove a config entry from a device."""
    return True
