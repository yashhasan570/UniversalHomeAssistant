"""Config flow."""

from universalassistant.config_entries import ConfigFlow
from universalassistant.core import __HAC_KEEP__


class MockConfigFlow(
    ConfigFlow, domain="test_package_raises_cancelled_error_config_entry"
):
    """Mock config flow."""


async def _async_has_devices(hass: __HAC_KEEP__) -> bool:
    """Return if there are devices that can be discovered."""
    return True
