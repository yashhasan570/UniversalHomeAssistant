"""Test the default_config init."""

from unittest.mock import patch

import pytest

from universalassistant import bootstrap
from universalassistant.components.default_config import DOMAIN
from universalassistant.components.universalassistant import DOMAIN as HOMEASSISTANT_DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import recorder as recorder_helper
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
def mock_ssdp():
    """Mock ssdp."""
    with (
        patch("universalassistant.components.ssdp.Scanner.async_scan"),
        patch("universalassistant.components.ssdp.Server.async_start"),
        patch("universalassistant.components.ssdp.Server.async_stop"),
    ):
        yield


@pytest.fixture(autouse=True)
def recorder_url_mock():
    """Mock recorder url."""
    with patch(
        "universalassistant.components.recorder.get_default_url", return_value="sqlite://"
    ):
        yield


@pytest.mark.usefixtures("mock_bluetooth", "mock_zeroconf", "socket_enabled")
async def test_setup(hass: UniversalAssistant) -> None:
    """Test setup."""
    recorder_helper.async_initialize_recorder(hass)
    # default_config needs the universalassistant integration, assert it will be
    # automatically setup by bootstrap and set it up manually for this test
    assert HOMEASSISTANT_DOMAIN in bootstrap.CORE_INTEGRATIONS
    assert await async_setup_component(hass, HOMEASSISTANT_DOMAIN, {"foo": "bar"})

    assert await async_setup_component(hass, DOMAIN, {"foo": "bar"})
