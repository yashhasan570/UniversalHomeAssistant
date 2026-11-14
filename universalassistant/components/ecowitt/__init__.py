"""The Ecowitt Weather Station Component."""

from aioecowitt import EcoWittListener
from aiohttp import web

from universalassistant.components import webhook
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_WEBHOOK_ID, EVENT_HOMEASSISTANT_STOP, Platform
from universalassistant.core import Event, UniversalAssistant, callback

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

type EcowittConfigEntry = ConfigEntry[EcoWittListener]


async def async_setup_entry(hass: UniversalAssistant, entry: EcowittConfigEntry) -> None:
    """Set up the Ecowitt component from UI."""
    ecowitt = entry.runtime_data = EcoWittListener()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_webhook(
        hass: UniversalAssistant, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle webhook callback."""
        return await ecowitt.handler(request)

    webhook.async_register(
        hass, DOMAIN, entry.title, entry.data[CONF_WEBHOOK_ID], handle_webhook
    )

    @callback
    def _stop_ecowitt(_: Event) -> None:
        """Stop the Ecowitt listener."""
        webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _stop_ecowitt)
    )


async def async_unload_entry(hass: UniversalAssistant, entry: EcowittConfigEntry) -> None:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
