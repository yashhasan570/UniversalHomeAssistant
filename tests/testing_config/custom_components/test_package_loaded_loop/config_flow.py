"""Config flow."""

from universalassistant.core import __HAC_KEEP__


async def _async_has_devices(hass: __HAC_KEEP__) -> bool:
    return True
