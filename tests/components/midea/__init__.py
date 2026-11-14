"""Tests for the Midea integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__

from .conftest import DummyDevice


async def setup_integration(
    hass: __HAC_KEEP__, config_entry: MockConfigEntry, device: DummyDevice
) -> None:
    """Set up a Midea config entry backed by a fake device."""
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.midea.device_selector",
        return_value=device,
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)

    await hass.async_block_till_done()
