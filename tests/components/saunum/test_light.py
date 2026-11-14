"""Test the Saunum light platform."""

from dataclasses import replace

from pysaunum import SaunumException
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


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.LIGHT]


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("service", "expected_state", "client_method", "expected_args"),
    [
        (SERVICE_TURN_ON, STATE_ON, "async_set_light_control", (True,)),
        (SERVICE_TURN_OFF, STATE_OFF, "async_set_light_control", (False,)),
    ],
)
@pytest.mark.usefixtures("init_integration")
async def test_light_service_calls(
    hass: __HAC_KEEP__,
    mock_saunum_client,
    service: str,
    expected_state: str,
    client_method: str,
    expected_args: tuple,
) -> None:
    """Test light service calls."""
    entity_id = "light.saunum_leil_light"

    # Mock the client method to update the coordinator data
    async def update_light_state(*args):
        """Update the light state in mock data."""
        current_data = mock_saunum_client.async_get_data.return_value
        mock_saunum_client.async_get_data.return_value = replace(
            current_data, light_on=(expected_state == STATE_ON)
        )

    getattr(mock_saunum_client, client_method).side_effect = update_light_state

    await hass.services.async_call(
        LIGHT_DOMAIN,
        service,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    getattr(mock_saunum_client, client_method).assert_called_once_with(*expected_args)

    # Verify state updated
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == expected_state


@pytest.mark.parametrize(
    ("service", "expected_error"),
    [
        (SERVICE_TURN_ON, "Failed to turn on light"),
        (SERVICE_TURN_OFF, "Failed to turn off light"),
    ],
)
@pytest.mark.usefixtures("init_integration")
async def test_light_service_call_failure(
    hass: __HAC_KEEP__,
    mock_saunum_client,
    service: str,
    expected_error: str,
) -> None:
    """Test handling of light service call failures."""
    entity_id = "light.saunum_leil_light"

    # Make the client method raise an exception
    mock_saunum_client.async_set_light_control.side_effect = SaunumException(
        "Connection lost"
    )

    with pytest.raises(__HAC_KEEP__Error, match=expected_error):
        await hass.services.async_call(
            LIGHT_DOMAIN,
            service,
            {ATTR_ENTITY_ID: entity_id},
            blocking=True,
        )
