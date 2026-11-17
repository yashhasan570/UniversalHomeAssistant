"""Test Wallbox Lock component."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.lock import LockService
from universalassistant.components.wallbox.coordinator import InsufficientRights
from universalassistant.const import TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError

from .conftest import http_403_error, http_404_error, http_429_error, setup_integration
from .const import MOCK_LOCK_ENTITY_ID


async def test_wallbox_lock_class(
    hass: UniversalAssistant, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox lock class."""

    await setup_integration(hass, entry)

    state = hass.states.get(MOCK_LOCK_ENTITY_ID)
    assert state
    assert state.state == "unlocked"

    await hass.services.async_call(
        "lock",
        LockService.LOCK,
        {
            TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
        },
        blocking=True,
    )

    await hass.services.async_call(
        "lock",
        LockService.UNLOCK,
        {
            TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
        },
        blocking=True,
    )


async def test_wallbox_lock_class_error_handling(
    hass: UniversalAssistant, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox lock class connection error."""

    await setup_integration(hass, entry)

    with (
        patch.object(mock_wallbox, "lockCharger", side_effect=http_404_error),
        pytest.raises(UniversalAssistantError),
    ):
        await hass.services.async_call(
            "lock",
            LockService.LOCK,
            {
                TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
            },
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "lockCharger", side_effect=http_404_error),
        patch.object(mock_wallbox, "unlockCharger", side_effect=http_404_error),
        pytest.raises(UniversalAssistantError),
    ):
        await hass.services.async_call(
            "lock",
            LockService.LOCK,
            {
                TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
            },
            blocking=True,
        )
    with (
        patch.object(mock_wallbox, "lockCharger", side_effect=http_404_error),
        patch.object(mock_wallbox, "unlockCharger", side_effect=http_404_error),
        pytest.raises(UniversalAssistantError),
    ):
        await hass.services.async_call(
            "lock",
            LockService.UNLOCK,
            {
                TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
            },
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "lockCharger", side_effect=http_403_error),
        patch.object(mock_wallbox, "unlockCharger", side_effect=http_403_error),
        pytest.raises(InsufficientRights),
    ):
        await hass.services.async_call(
            "lock",
            LockService.UNLOCK,
            {
                TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
            },
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "lockCharger", side_effect=http_429_error),
        patch.object(mock_wallbox, "unlockCharger", side_effect=http_429_error),
        pytest.raises(UniversalAssistantError),
    ):
        await hass.services.async_call(
            "lock",
            LockService.UNLOCK,
            {
                TargetKey.ENTITY_ID: MOCK_LOCK_ENTITY_ID,
            },
            blocking=True,
        )
