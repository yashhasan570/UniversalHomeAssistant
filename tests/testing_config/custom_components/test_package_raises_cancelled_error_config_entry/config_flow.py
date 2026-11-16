"""Config flow."""

from universalassistant.config_entries import ConfigFlow
from universalassistant.core import UniversalAssistant


class MockConfigFlow(
    ConfigFlow, domain="test_package_raises_cancelled_error_config_entry"
):
    """Mock config flow."""


async def _async_has_devices(hass: UniversalAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    return True
