"""Tests for the NRGkick integration."""

from collections.abc import Iterable
from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


async def setup_integration(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    platforms: Iterable[Platform] | None = None,
) -> None:
    """Set up the component for tests."""
    config_entry.add_to_hass(hass)

    if platforms is None:
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        return

    with patch("universalassistant.components.nrgkick.PLATFORMS", list(platforms)):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
