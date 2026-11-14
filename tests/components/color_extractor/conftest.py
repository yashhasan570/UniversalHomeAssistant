"""Common fixtures for the Color extractor tests."""

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.color_extractor.const import DOMAIN
from universalassistant.core import UniversalAssistant


@pytest.fixture
async def config_entry() -> MockConfigEntry:
    """Mock config entry."""
    return MockConfigEntry(domain=DOMAIN, data={})


@pytest.fixture
async def setup_integration(hass: UniversalAssistant, config_entry: MockConfigEntry) -> None:
    """Add config entry for color extractor."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
