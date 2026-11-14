"""The switch tests for the tado platform."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from universalassistant.components.tado import DOMAIN
from universalassistant.const import ATTR_ENTITY_ID, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

CHILD_LOCK_SWITCH_ENTITY = "switch.baseboard_heater_baseboard_heater_child_lock"


@pytest.fixture(autouse=True)
def setup_platforms() -> Generator[None]:
    """Set up the platforms for the tests."""
    with patch("universalassistant.components.tado.PLATFORMS", [Platform.SWITCH]):
        yield


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: __HAC_KEEP__, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test creation of switch entities."""

    config_entry: MockConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.parametrize(
    ("method", "expected"), [(SERVICE_TURN_ON, True), (SERVICE_TURN_OFF, False)]
)
@pytest.mark.usefixtures("init_integration")
async def test_set_child_lock(hass: __HAC_KEEP__, method, expected) -> None:
    """Test enable child lock on switch."""

    with patch(
        "universalassistant.components.tado.PyTado.interface.api.Tado.set_child_lock"
    ) as mock_set_state:
        await hass.services.async_call(
            SWITCH_DOMAIN,
            method,
            {ATTR_ENTITY_ID: CHILD_LOCK_SWITCH_ENTITY},
            blocking=True,
        )

    mock_set_state.assert_called_once()
    assert mock_set_state.call_args[0][1] is expected
