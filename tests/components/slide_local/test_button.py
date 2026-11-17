"""Tests for the Slide Local button platform."""

from unittest.mock import AsyncMock

from goslideapi.goslideapi import (
    AuthenticationFailed,
    ClientConnectionError,
    ClientTimeoutError,
    DigestAuthCalcError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_platform


async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    await setup_platform(hass, mock_config_entry, [Platform.BUTTON])

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_pressing_button(
    hass: UniversalAssistant,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing button."""
    await setup_platform(hass, mock_config_entry, [Platform.BUTTON])

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            TargetKey.ENTITY_ID: "button.slide_bedroom_calibrate",
        },
        blocking=True,
    )
    mock_slide_api.slide_calibrate.assert_called_once()


@pytest.mark.parametrize(
    ("exception"),
    [
        ClientConnectionError,
        ClientTimeoutError,
        AuthenticationFailed,
        DigestAuthCalcError,
    ],
)
async def test_pressing_button_exception(
    hass: UniversalAssistant,
    exception: Exception,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing button."""
    await setup_platform(hass, mock_config_entry, [Platform.BUTTON])

    mock_slide_api.slide_calibrate.side_effect = exception

    with pytest.raises(
        UniversalAssistantError,
        match="Error while sending the calibration request to the device",
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                TargetKey.ENTITY_ID: "button.slide_bedroom_calibrate",
            },
            blocking=True,
        )
