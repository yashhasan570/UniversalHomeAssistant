"""The Modem Caller ID integration."""

from phone_modem import PhoneModem

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_DEVICE, EVENT_HOMEASSISTANT_STOP, Platform
from universalassistant.core import Event, UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

from .const import EXCEPTIONS

PLATFORMS = [Platform.BUTTON, Platform.SENSOR]

type ModemCallerIdConfigEntry = ConfigEntry[PhoneModem]


async def async_setup_entry(
    hass: UniversalAssistant, entry: ModemCallerIdConfigEntry
) -> None:
    """Set up Modem Caller ID from a config entry."""
    device = entry.data[CONF_DEVICE]
    api = PhoneModem(device)
    try:
        await api.initialize(device)
    except EXCEPTIONS as ex:
        raise ConfigEntryNotReady(f"Unable to open port: {device}") from ex

    entry.async_on_unload(api.close)

    async def _async_on_hass_stop(event: Event) -> None:
        """HA is shutting down, close modem port."""
        api.close()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_on_hass_stop)
    )

    entry.runtime_data = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: ModemCallerIdConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
