"""Test the FastdotcomDataUpdateCoordindator."""

from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.fastdotcom.const import DEFAULT_NAME, DOMAIN
from universalassistant.core import UniversalAssistant

from . import MOCK_DATA


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

    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=MOCK_DATA,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.fast_com_download")
    assert state is not None
    assert state.state == "100.0"
