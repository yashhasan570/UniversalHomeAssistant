"""Common fixtures for the Novy Cooker Hood tests."""

from collections.abc import Iterator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.radio_frequency.common import (
    MockRadioFrequencyEntity,
)

from universalassistant.components.novy_cooker_hood.const import CONF_TRANSMITTER, DOMAIN
from universalassistant.const import CONF_CODE
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

TRANSMITTER_ENTITY_ID = "radio_frequency.test_rf_transmitter"


@pytest.fixture(autouse=True)
def mock_command_delay() -> Iterator[None]:
    """Drop the inter-command delay so tests don't spend real time waiting."""
    with patch("universalassistant.components.novy_cooker_hood.fan._COMMAND_DELAY", 0):
        yield


@pytest.fixture
def mock_config_entry(
    mock_rf_entity: MockRadioFrequencyEntity,
    entity_registry: er.EntityRegistry,
) -> MockConfigEntry:
    """Return a mock config entry for Novy Cooker Hood."""
    entity_entry = entity_registry.async_get(TRANSMITTER_ENTITY_ID)
    assert entity_entry is not None
    return MockConfigEntry(
        domain=DOMAIN,
        title="Novy Cooker Hood",
        data={CONF_TRANSMITTER: TRANSMITTER_ENTITY_ID, CONF_CODE: 1},
        unique_id=f"{entity_entry.id}_1",
        minor_version=2,
    )


@pytest.fixture
async def init_novy_cooker_hood(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the Novy Cooker Hood integration."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry
