"""Test the WS66i 6-Zone Amplifier init file."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.ws66i.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from .test_media_player import (
    MOCK_CONFIG,
    MOCK_DEFAULT_OPTIONS,
    MOCK_OPTIONS,
    MockWs66i,
)

ZONE_1_ID = "media_player.zone_11"


async def test_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test connection error."""
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, options=MOCK_OPTIONS
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.ws66i.get_ws66i",
        new=lambda *a: MockWs66i(fail_open=True),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_RETRY
        assert hass.states.get(ZONE_1_ID) is None


async def test_cannot_connect_2(hass: __HAC_KEEP__) -> None:
    """Test connection error pt 2."""
    # Another way to test same case as test_cannot_connect
    ws66i = MockWs66i()
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, options=MOCK_DEFAULT_OPTIONS
    )
    config_entry.add_to_hass(hass)

    with patch.object(MockWs66i, "open", side_effect=ConnectionError):
        with patch(
            "universalassistant.components.ws66i.get_ws66i",
            new=lambda *a: ws66i,
        ):
            await hass.config_entries.async_setup(config_entry.entry_id)
            await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_RETRY
        assert hass.states.get(ZONE_1_ID) is None


async def test_unload_config_entry(hass: __HAC_KEEP__) -> None:
    """Test unloading config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, options=MOCK_OPTIONS
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.ws66i.get_ws66i",
        new=lambda *a: MockWs66i(),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    with patch.object(MockWs66i, "close") as method_call:
        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        assert method_call.called

    assert config_entry.state is ConfigEntryState.NOT_LOADED
