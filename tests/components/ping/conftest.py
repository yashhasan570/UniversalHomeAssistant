"""Test configuration for ping."""

from unittest.mock import patch

from icmplib import Host
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.device_tracker import CONF_CONSIDER_HOME
from universalassistant.components.ping import CONF_PING_COUNT, DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant


@pytest.fixture
def patch_setup(*args, **kwargs):
    """Patch setup methods."""
    with (
        patch(
            "universalassistant.components.ping.async_setup_entry",
            return_value=None,
        ),
        patch("universalassistant.components.ping.async_setup", return_value=True),
    ):
        yield


@pytest.fixture(autouse=True)
async def patch_ping():
    """Patch icmplib async_ping."""
    mock = Host("10.10.10.10", 5, [10, 1, 2, 5, 6])

    with (
        patch("universalassistant.components.ping.helpers.async_ping", return_value=mock),
        patch("universalassistant.components.ping.async_ping", return_value=mock),
    ):
        yield mock


@pytest.fixture(name="config_entry")
async def mock_config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Return a MockConfigEntry for testing."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="10.10.10.10",
        entry_id="01JPING0000000000000000000",
        options={
            CONF_HOST: "10.10.10.10",
            CONF_PING_COUNT: 10.0,
            CONF_CONSIDER_HOME: 180,
        },
    )


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: UniversalAssistant, config_entry: MockConfigEntry, patch_ping
) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
