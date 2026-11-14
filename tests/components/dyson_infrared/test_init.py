"""Tests for the Dyson Infrared config entry setup/unload."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.dyson_infrared import PLATFORMS
from universalassistant.core import __HAC_KEEP__


async def test_async_setup_entry(hass: __HAC_KEEP__) -> None:
    """Test setting up the Dyson Infrared config entry."""
    entry = MockConfigEntry(domain="dyson_infrared")
    entry.add_to_hass(hass)

    with patch.object(
        hass.config_entries, "async_forward_entry_setups"
    ) as mock_forward:
        result = await hass.config_entries.async_setup(entry.entry_id)

        assert result is True
        mock_forward.assert_called_once_with(entry, PLATFORMS)


async def test_async_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test unloading a config entry forwards unload to platforms."""
    entry = MockConfigEntry(domain="dyson_infrared")
    entry.add_to_hass(hass)

    with patch.object(hass.config_entries, "async_forward_entry_setups"):
        await hass.config_entries.async_setup(entry.entry_id)

    with patch.object(
        hass.config_entries, "async_unload_platforms", return_value=True
    ) as mock_unload:
        result = await hass.config_entries.async_unload(entry.entry_id)

        assert result is True
        mock_unload.assert_called_once_with(entry, PLATFORMS)
