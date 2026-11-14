"""Test AirVisual Pro setup."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.airvisual_pro.const import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr


async def test_device_registry(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    pro: Mock,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the device registry entry, including the network MAC connection."""
    with patch("universalassistant.components.airvisual_pro.NodeSamba", return_value=pro):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    device_entry = device_registry.async_get_device_by_identifier(
        (DOMAIN, "XXXXXXX"), config_entry.entry_id
    )
    assert device_entry == snapshot
