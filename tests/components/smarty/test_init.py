"""Tests for the Smarty component."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.smarty.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from . import setup_integration


async def test_device(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_smarty: AsyncMock,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test device."""
    await setup_integration(hass, mock_config_entry)
    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, mock_config_entry.entry_id), mock_config_entry.entry_id
    )
    assert device
    assert device == snapshot
