"""Test the Foscam number platform."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.foscam.const import DOMAIN
from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .conftest import setup_mock_foscam_camera
from .const import ENTRY_ID, VALID_CONFIG


async def test_number_entities(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test creation of number entities."""
    entry = MockConfigEntry(domain=DOMAIN, data=VALID_CONFIG, entry_id=ENTRY_ID)
    entry.add_to_hass(hass)

    with (
        # Mock a valid camera instance
        patch("universalassistant.components.foscam.FoscamCamera") as mock_foscam_camera,
        patch("universalassistant.components.foscam.PLATFORMS", [Platform.NUMBER]),
    ):
        setup_mock_foscam_camera(mock_foscam_camera)
        assert await hass.config_entries.async_setup(entry.entry_id)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_setting_number(hass: __HAC_KEEP__) -> None:
    """Test setting a number entity calls the correct method on the camera."""
    entry = MockConfigEntry(domain=DOMAIN, data=VALID_CONFIG, entry_id=ENTRY_ID)
    entry.add_to_hass(hass)

    with patch("universalassistant.components.foscam.FoscamCamera") as mock_foscam_camera:
        setup_mock_foscam_camera(mock_foscam_camera)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.mock_title_device_volume",
                NumberServiceArgument.VALUE: 42,
            },
            blocking=True,
        )
        mock_foscam_camera.setAudioVolume.assert_called_once_with(42)
