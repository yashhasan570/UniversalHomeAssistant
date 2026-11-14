"""Test time entities for the LetPot integration."""

from datetime import time
from unittest.mock import MagicMock, patch

from letpot.exceptions import LetPotConnectionException, LetPotException
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.time import TimeService
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test time entities."""
    with patch("universalassistant.components.letpot.PLATFORMS", [Platform.TIME]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_set_time(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    device_type: str,
) -> None:
    """Test setting the time entity."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        "time",
        TimeService.SET_VALUE,
        service_data={"time": time(hour=7, minute=0)},
        blocking=True,
        target={"entity_id": "time.garden_light_on"},
    )

    mock_device_client.set_light_schedule.assert_awaited_once_with(
        f"{device_type}ABCD", time(7, 0), None
    )


@pytest.mark.parametrize(
    ("exception", "user_error"),
    [
        (
            LetPotConnectionException("Connection failed"),
            "An error occurred while communicating with the LetPot"
            " device: Connection failed",
        ),
        (
            LetPotException("Random thing failed"),
            "An unknown error occurred while communicating with"
            " the LetPot device: Random thing failed",
        ),
    ],
)
async def test_time_error(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    exception: Exception,
    user_error: str,
) -> None:
    """Test time entity exception handling."""
    await setup_integration(hass, mock_config_entry)

    mock_device_client.set_light_schedule.side_effect = exception

    assert hass.states.get("time.garden_light_on") is not None
    with pytest.raises(__HAC_KEEP__Error, match=user_error):
        await hass.services.async_call(
            "time",
            TimeService.SET_VALUE,
            service_data={"time": time(hour=7, minute=0)},
            blocking=True,
            target={"entity_id": "time.garden_light_on"},
        )
