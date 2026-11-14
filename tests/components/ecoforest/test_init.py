"""Tests for the Ecoforest integration setup."""

from unittest.mock import patch

from pyecoforest.exceptions import EcoforestAuthenticationRequired
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


async def test_setup_authentication_failed(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry
) -> None:
    """Test setup fails when authentication on the device fails."""
    with patch(
        "pyecoforest.api.EcoforestApi.get",
        side_effect=EcoforestAuthenticationRequired("401"),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_ERROR
    assert config_entry.reason == "Authentication on device 1.1.1.1 failed"
