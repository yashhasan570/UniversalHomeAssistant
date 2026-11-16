"""Tests for Renault binary sensors."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.usefixtures("patch_renault_account", "patch_get_vehicles")


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("universalassistant.components.renault.PLATFORMS", [Platform.BINARY_SENSOR]):
        yield


@pytest.mark.usefixtures("fixtures_with_data")
async def test_binary_sensors(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_no_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_empty(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors with empty data from Renault."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_invalid_upstream_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_errors(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors with temporary failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_access_denied_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_access_denied(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault binary sensors with access denied failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0


@pytest.mark.usefixtures("fixtures_with_not_supported_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_not_supported(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault binary sensors with not supported failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0
