"""Test the Kiosker binary sensors."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_kiosker_api: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    mock_kiosker_api.blackout_get.return_value = SimpleNamespace(
        visible=True, dismissible=True
    )
    mock_kiosker_api.screensaver_get_state.return_value = SimpleNamespace(visible=False)

    with patch("universalassistant.components.kiosker._PLATFORMS", [Platform.BINARY_SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
