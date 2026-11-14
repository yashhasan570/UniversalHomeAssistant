"""Tests for the Huum light entity."""

from unittest.mock import AsyncMock, patch

from huum.exceptions import RequestError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.light import DOMAIN as LIGHT_DOMAIN
from universalassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

ENTITY_ID = "light.huum_sauna_light"


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.LIGHT]


@pytest.mark.usefixtures("init_integration")
async def test_light(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the initial parameters."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("init_integration")
async def test_light_turn_off(
    hass: __HAC_KEEP__,
    mock_huum_client: AsyncMock,
) -> None:
    """Test turning off light."""
    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_ON

    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )
    mock_huum_client.toggle_light.assert_awaited_once()


async def test_light_turn_on(
    hass: __HAC_KEEP__,
    mock_huum_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test turning on light."""
    mock_huum_client.status.return_value.light = 0

    mock_config_entry.add_to_hass(hass)
    with patch("universalassistant.components.huum.PLATFORMS", [Platform.LIGHT]):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_OFF

    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )
    mock_huum_client.toggle_light.assert_awaited_once()


@pytest.mark.usefixtures("init_integration")
async def test_light_communication_error(
    hass: __HAC_KEEP__,
    mock_huum_client: AsyncMock,
) -> None:
    """Test that API errors when toggling the light are raised as __HAC_KEEP__Error."""
    mock_huum_client.toggle_light.side_effect = RequestError()

    with pytest.raises(
        __HAC_KEEP__Error,
        match="An error occurred while communicating with the Huum sauna",
    ):
        await hass.services.async_call(
            LIGHT_DOMAIN,
            SERVICE_TURN_OFF,
            {ATTR_ENTITY_ID: ENTITY_ID},
            blocking=True,
        )
