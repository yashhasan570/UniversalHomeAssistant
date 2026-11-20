"""Test Tuya camera platform."""

from typing import Any
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion
from tuya_sharing import CustomerDevice, Manager

from universalassistant.components.camera import DOMAIN as CAMERA_DOMAIN, CameraService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import initialize_entry


@pytest.fixture(autouse=True)
def platform_autouse():
    """Platform fixture."""
    with (
        patch("universalassistant.components.tuya.PLATFORMS", [Platform.CAMERA]),
        # Mock camera access token which normally is randomized.
        patch(
            "universalassistant.components.camera.entity.SystemRandom.getrandbits",
            return_value=1,
        ),
    ):
        yield


@pytest.mark.usefixtures("no_quirk")
async def test_platform_setup_and_discovery(
    hass: UniversalAssistant,
    mock_manager: Manager,
    mock_config_entry: MockConfigEntry,
    mock_devices: list[CustomerDevice],
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test platform setup and discovery."""

    await initialize_entry(hass, mock_manager, mock_config_entry, mock_devices)

    await snapshot_platform(
        hass,
        entity_registry,
        snapshot,
        mock_config_entry.entry_id,
    )


@pytest.mark.parametrize(
    "mock_device_code",
    ["sp_rudejjigkywujjvs"],
)
@pytest.mark.parametrize(
    ("service", "expected_command"),
    [
        (
            CameraService.DISABLE_MOTION_DETECTION,
            {"code": "motion_switch", "value": False},
        ),
        (
            CameraService.ENABLE_MOTION_DETECTION,
            {"code": "motion_switch", "value": True},
        ),
    ],
)
async def test_action(
    hass: UniversalAssistant,
    mock_manager: Manager,
    mock_config_entry: MockConfigEntry,
    mock_device: CustomerDevice,
    service: str,
    expected_command: dict[str, Any],
) -> None:
    """Test camera action."""
    entity_id = "camera.burocam"
    await initialize_entry(hass, mock_manager, mock_config_entry, mock_device)

    state = hass.states.get(entity_id)
    assert state is not None, f"{entity_id} does not exist"
    await hass.services.async_call(
        CAMERA_DOMAIN,
        service,
        {
            TargetKey.ENTITY_ID: entity_id,
        },
        blocking=True,
    )
    mock_manager.send_commands.assert_called_once_with(
        mock_device.id, [expected_command]
    )
