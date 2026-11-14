"""Tests for miele switch module."""

from unittest.mock import MagicMock, Mock

from aiohttp import ClientResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platforms", [(Platform.SWITCH,)])

ENTITY_ID = "switch.freezer_superfreezing"


async def test_switch_states(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test switch entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_switch_states_api_push(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
    push_data_and_actions: None,
) -> None:
    """Test switch state when the API pushes data via SSE."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.parametrize(
    ("entity"),
    [
        (ENTITY_ID),
        ("switch.refrigerator_supercooling"),
        ("switch.washing_machine_power"),
    ],
)
@pytest.mark.parametrize(
    ("service"),
    [
        (SERVICE_TURN_ON),
        (SERVICE_TURN_OFF),
    ],
)
async def test_switching(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
    service: str,
    entity: str,
) -> None:
    """Test the switch can be turned on/off."""

    await hass.services.async_call(
        SWITCH_DOMAIN, service, {ATTR_ENTITY_ID: entity}, blocking=True
    )
    mock_miele_client.send_action.assert_called_once()


@pytest.mark.parametrize(
    ("entity"),
    [
        (ENTITY_ID),
        ("switch.refrigerator_supercooling"),
        ("switch.washing_machine_power"),
    ],
)
@pytest.mark.parametrize(
    ("service"),
    [
        (SERVICE_TURN_ON),
        (SERVICE_TURN_OFF),
    ],
)
async def test_api_failure(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
    service: str,
    entity: str,
) -> None:
    """Test handling of exception from API."""
    mock_miele_client.send_action.side_effect = ClientResponseError(Mock(), Mock())

    with pytest.raises(__HAC_KEEP__Error, match=f"Failed to set state for {entity}"):
        await hass.services.async_call(
            SWITCH_DOMAIN, service, {ATTR_ENTITY_ID: entity}, blocking=True
        )
    mock_miele_client.send_action.assert_called_once()
