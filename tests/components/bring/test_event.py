"""Test for event platform of the Bring! integration."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def event_only() -> Generator[None]:
    """Enable only the event platform."""
    with patch(
        "universalassistant.components.bring.PLATFORMS",
        [Platform.EVENT],
    ):
        yield


@pytest.mark.freeze_time("2025-01-01T03:30:00.000Z")
@pytest.mark.usefixtures("mock_bring_client")
async def test_setup(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Snapshot test states of event platform."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(
        hass, entity_registry, snapshot, bring_config_entry.entry_id
    )
