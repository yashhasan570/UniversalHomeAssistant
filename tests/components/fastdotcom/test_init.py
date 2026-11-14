"""Test for Sensibo component Init."""

from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.fastdotcom.const import DEFAULT_NAME, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import EVENT_HOMEASSISTANT_STARTED, STATE_UNKNOWN
from universalassistant.core import CoreState, __HAC_KEEP__

from . import MOCK_DATA


async def test_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test unload an entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="UNIQUE_TEST_ID",
        title=DEFAULT_NAME,
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=MOCK_DATA,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED
    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_delayed_speedtest_during_startup(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Test delayed speedtest during startup."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="UNIQUE_TEST_ID",
        title=DEFAULT_NAME,
    )
    config_entry.add_to_hass(hass)

    original_state = hass.state
    hass.set_state(CoreState.starting)
    with patch("universalassistant.components.fastdotcom.coordinator.fast_com"):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
    hass.set_state(original_state)

    assert config_entry.state is ConfigEntryState.LOADED
    state = hass.states.get("sensor.fast_com_download")
    # Assert state is Unknown as fast.com isn't starting until HA has started
    assert state.state is STATE_UNKNOWN

    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=MOCK_DATA,
    ):
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.fast_com_download")
    assert state is not None
    assert state.state == "100.0"
    assert config_entry.state is ConfigEntryState.LOADED
