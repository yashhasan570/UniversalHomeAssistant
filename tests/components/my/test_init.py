"""Test the my init."""

from unittest import mock

from universalassistant.components.my import DOMAIN, URL_PATH
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_setup(hass: UniversalAssistant) -> None:
    """Test setup."""
    with mock.patch(
        "universalassistant.components.frontend.async_register_built_in_panel"
    ) as mock_register_panel:
        assert await async_setup_component(hass, DOMAIN, {"foo": "bar"})
        assert mock_register_panel.call_args == mock.call(
            hass, "my", frontend_url_path=URL_PATH
        )
