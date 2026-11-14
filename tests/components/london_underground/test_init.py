"""Test the London Underground init."""

from universalassistant.core import UniversalAssistant


async def test_reload_entry(
    hass: UniversalAssistant, mock_london_underground_client, mock_config_entry
) -> None:
    """Test reloading the config entry."""

    # Test reloading with updated options
    hass.config_entries.async_update_entry(
        mock_config_entry,
        data={},
        options={"line": ["Bakerloo", "Central"]},
    )
    await hass.async_block_till_done()

    # Verify that setup was called for each reload
    assert len(mock_london_underground_client.mock_calls) > 0
