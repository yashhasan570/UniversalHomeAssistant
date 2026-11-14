"""Test the IPMA integration."""

from unittest.mock import patch

from pyipma import IPMAException
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.ipma.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_MODE
from universalassistant.core import __HAC_KEEP__

from .test_weather import MockLocation


async def test_async_setup_raises_entry_not_ready(hass: __HAC_KEEP__) -> None:
    """Test that it throws ConfigEntryNotReady when exception occurs during setup."""

    with patch(
        "pyipma.location.Location.get", side_effect=IPMAException("API unavailable")
    ):
        config_entry = MockConfigEntry(
            domain=DOMAIN,
            title="Home",
            data={CONF_LATITUDE: 0, CONF_LONGITUDE: 0, CONF_MODE: "daily"},
        )

        config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(config_entry.entry_id)

        assert config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_config_entry(hass: __HAC_KEEP__) -> None:
    """Test entry unloading."""

    with patch(
        "pyipma.location.Location.get",
        return_value=MockLocation(),
    ):
        config_entry = MockConfigEntry(
            domain=DOMAIN,
            data={CONF_LATITUDE: 0, CONF_LONGITUDE: 0, CONF_MODE: "daily"},
        )
        config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.LOADED

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.NOT_LOADED
