"""Test the FastdotcomDataUpdateCoordindator."""

from datetime import timedelta
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.fastdotcom.const import DEFAULT_NAME, DOMAIN
from universalassistant.components.fastdotcom.coordinator import DEFAULT_INTERVAL
from universalassistant.const import STATE_UNAVAILABLE
from universalassistant.core import UniversalAssistant


async def test_fastdotcom_data_update_coordinator(
    hass: UniversalAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Test the update coordinator."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="UNIQUE_TEST_ID",
        title=DEFAULT_NAME,
    )
    config_entry.add_to_hass(hass)

    mock_data = {
        "download_speed": 5.0,
        "upload_speed": 50.0,
        "unloaded_ping": 15.2,
        "loaded_ping": 20.2,
    }
    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=mock_data,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.fast_com_download")
    assert state is not None
    assert state.state == "5.0"

    mock_data = {
        "download_speed": 10.0,
        "upload_speed": 20.0,
        "unloaded_ping": 5.0,
        "loaded_ping": 20.0,
    }
    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=mock_data,
    ):
        freezer.tick(timedelta(hours=DEFAULT_INTERVAL))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.fast_com_download")
    assert state.state == "10.0"

    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        side_effect=Exception("Test error"),
    ):
        freezer.tick(timedelta(hours=DEFAULT_INTERVAL))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.fast_com_download")
    assert state.state is STATE_UNAVAILABLE
