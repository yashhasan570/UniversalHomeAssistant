"""Test the SFR Box sensors."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.usefixtures(
    "system_get_info", "dsl_get_info", "voip_get_info", "wan_get_info"
)


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with (
        patch("universalassistant.components.sfr_box.PLATFORMS", [Platform.SENSOR]),
        patch("universalassistant.components.sfr_box.coordinator.SFRBox.authenticate"),
    ):
        yield


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors(
    hass: __HAC_KEEP__,
    config_entry_with_auth: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for SFR Box sensors."""
    await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(
        hass, entity_registry, snapshot, config_entry_with_auth.entry_id
    )


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_no_auth(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for SFR Box sensors."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Ensure auth-only entities are not registered
    assert sorted(entity_registry.entities) == snapshot
