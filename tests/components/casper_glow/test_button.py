"""Test the Casper Glow button platform."""

from unittest.mock import MagicMock, patch

from pycasperglow import CasperGlowError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration

PAUSE_ENTITY_ID = "button.jar_pause_dimming"
RESUME_ENTITY_ID = "button.jar_resume_dimming"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_entities(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_casper_glow: MagicMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test all button entities match the snapshot."""
    with patch("universalassistant.components.casper_glow.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "method"),
    [
        (PAUSE_ENTITY_ID, "pause"),
        (RESUME_ENTITY_ID, "resume"),
    ],
)
async def test_button_press_calls_device(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_casper_glow: MagicMock,
    entity_id: str,
    method: str,
) -> None:
    """Test that pressing a button calls the correct device method."""
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: entity_id},
        blocking=True,
    )

    getattr(mock_casper_glow, method).assert_called_once()


@pytest.mark.parametrize(
    ("entity_id", "method"),
    [
        (PAUSE_ENTITY_ID, "pause"),
        (RESUME_ENTITY_ID, "resume"),
    ],
)
async def test_button_raises_universalassistant_error_on_failure(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_casper_glow: MagicMock,
    entity_id: str,
    method: str,
) -> None:
    """Test that a CasperGlowError is converted to UniversalAssistantError."""
    getattr(mock_casper_glow, method).side_effect = CasperGlowError("connection lost")

    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {TargetKey.ENTITY_ID: entity_id},
            blocking=True,
        )
