"""Test Wallbox Button component."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.wallbox.coordinator import InsufficientRights
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error

from .conftest import http_403_error, http_404_error, http_429_error, setup_integration
from .const import MOCK_BUTTON_RESUME_SCHEDULE_ID


async def test_wallbox_button_resume_schedule(
    hass: __HAC_KEEP__, entry: MockConfigEntry, mock_wallbox: MagicMock
) -> None:
    """Test pressing the resume schedule button calls the Wallbox API once."""

    await setup_integration(hass, entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: MOCK_BUTTON_RESUME_SCHEDULE_ID},
        blocking=True,
    )

    mock_wallbox.resumeSchedule.assert_called_once()


async def test_wallbox_button_resume_schedule_error_handling(
    hass: __HAC_KEEP__, entry: MockConfigEntry, mock_wallbox: MagicMock
) -> None:
    """Test button error handling for 403, 429 and other HTTP errors."""

    await setup_integration(hass, entry)

    with (
        patch.object(mock_wallbox, "resumeSchedule", side_effect=http_403_error),
        pytest.raises(InsufficientRights),
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: MOCK_BUTTON_RESUME_SCHEDULE_ID},
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "resumeSchedule", side_effect=http_429_error),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: MOCK_BUTTON_RESUME_SCHEDULE_ID},
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "resumeSchedule", side_effect=http_404_error),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: MOCK_BUTTON_RESUME_SCHEDULE_ID},
            blocking=True,
        )
