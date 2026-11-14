"""Test Govee lights local diagnostics."""

from unittest.mock import AsyncMock

from govee_local_api.message import DevStatusResponse
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from .conftest import SCENE_CAPABILITIES, setup_light


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_govee_api: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    entry, device = await setup_light(hass, mock_govee_api, SCENE_CAPABILITIES)
    device.update(
        DevStatusResponse(
            {
                "onOff": 1,
                "brightness": 80,
                "color": {"r": 255, "g": 128, "b": 0},
                "colorTemInKelvin": 0,
            }
        )
    )

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
