"""Test the Nightscout config flow."""

from unittest.mock import patch

from aiohttp import ClientError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.nightscout.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_URL, STATE_UNAVAILABLE
from universalassistant.core import UniversalAssistant

from . import SERVER_STATUS, init_integration, init_integration_empty_response


async def test_unload_entry(hass: UniversalAssistant) -> None:
    """Test successful unload of entry."""
    entry = await init_integration(hass)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)


async def test_async_setup_raises_entry_not_ready(hass: UniversalAssistant) -> None:
    """Test that it throws ConfigEntryNotReady when exception occurs during setup."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_URL: "https://some.url:1234"},
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.nightscout.NightscoutAPI.get_server_status",
        side_effect=ClientError(),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
    assert config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_without_readings(hass: UniversalAssistant) -> None:
    """Test setup succeeds when the server returns no glucose readings."""
    config_entry = await init_integration_empty_response(hass)

    assert config_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.blood_sugar").state == STATE_UNAVAILABLE


async def test_first_refresh_error_raises_entry_not_ready(
    hass: UniversalAssistant,
) -> None:
    """Test setup is retried when the first glucose fetch fails."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_URL: "https://some.url:1234"},
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.nightscout.NightscoutAPI.get_server_status",
            return_value=SERVER_STATUS,
        ),
        patch(
            "universalassistant.components.nightscout.NightscoutAPI.get_sgvs",
            side_effect=ClientError(),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
    assert config_entry.state is ConfigEntryState.SETUP_RETRY
