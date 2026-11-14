"""Test the Seafile button platform."""

from unittest.mock import AsyncMock, patch

from aioseafile import (
    SeafileConnectionError,
    SeafilePermissionError,
    SeafileTimeoutError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration
from .conftest import LIBRARY_ID

EMPTY_TRASH = "button.documents_empty_trash"


@pytest.mark.usefixtures("mock_seafile_client")
async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all button entities."""
    with patch("universalassistant.components.seafile.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_empty_trash(
    hass: UniversalAssistant,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing the button empties the trash of the library."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: EMPTY_TRASH},
        blocking=True,
    )

    mock_seafile_client.clean_library_trash.assert_awaited_once_with(LIBRARY_ID)


@pytest.mark.parametrize(
    ("exception", "translation_key"),
    [
        pytest.param(SeafilePermissionError, "permission_denied", id="not_allowed"),
        pytest.param(SeafileTimeoutError, "timeout_connect", id="timeout"),
        pytest.param(SeafileConnectionError, "api_error", id="failed"),
    ],
)
async def test_empty_trash_errors(
    hass: UniversalAssistant,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    exception: type[Exception],
    translation_key: str,
) -> None:
    """Test errors while emptying the trash are raised as translated errors."""
    await setup_integration(hass, mock_config_entry)
    mock_seafile_client.clean_library_trash.side_effect = exception

    with pytest.raises(UniversalAssistantError) as exc_info:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: EMPTY_TRASH},
            blocking=True,
        )
    assert exc_info.value.translation_key == translation_key
