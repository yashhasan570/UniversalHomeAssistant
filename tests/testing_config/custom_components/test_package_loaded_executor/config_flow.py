"""Config flow."""

from universalassistant.core import UniversalAssistant


async def _async_has_devices(hass: UniversalAssistant) -> bool:
    return True
