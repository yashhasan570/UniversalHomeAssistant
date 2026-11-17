"""Tests for time."""

from unittest.mock import MagicMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.time import (
    DOMAIN as TIME_DOMAIN,
    TimeService,
    TimeServiceArgument,
)
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_time(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
) -> None:
    """Test the Ohme sensors."""
    with patch("universalassistant.components.ohme.PLATFORMS", [Platform.TIME]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_set_time(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
) -> None:
    """Test the time set."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        TIME_DOMAIN,
        TimeService.SET_VALUE,
        service_data={
            TimeServiceArgument.TIME: "00:00:00",
        },
        target={
            TargetKey.ENTITY_ID: "time.ohme_home_pro_target_time",
        },
        blocking=True,
    )

    assert len(mock_client.async_set_target.mock_calls) == 1
