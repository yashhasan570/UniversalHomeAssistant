"""The tests for the WSDOT platform."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import issue_registry as ir


async def test_travel_sensor_setup_no_auth(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_failed_travel_time: None,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test the wsdot Travel Time sensor does not create an entry with a bad API key."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
