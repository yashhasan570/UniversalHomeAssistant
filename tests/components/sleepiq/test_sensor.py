"""The tests for SleepIQ sensor platform."""

from unittest.mock import MagicMock

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from universalassistant.const import STATE_UNKNOWN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .conftest import BED_NAME_LOWER, SLEEPER_L_NAME_LOWER, setup_platform


async def test_sensors(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_asyncsleepiq,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the SleepIQ sleepnumber for a bed with two sides."""
    entry = await setup_platform(hass, SENSOR_DOMAIN)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


@pytest.mark.parametrize(
    "timezone",
    [pytest.param(None, id="missing"), pytest.param("Not/AZone", id="invalid")],
)
async def test_session_times_without_bed_timezone(
    hass: UniversalAssistant,
    mock_asyncsleepiq: MagicMock,
    mock_bed: MagicMock,
    timezone: str | None,
) -> None:
    """Test session times stay unknown when the bed time zone is not usable."""
    mock_bed.timezone = timezone
    await setup_platform(hass, SENSOR_DOMAIN)

    assert (
        hass.states.get(
            f"sensor.{BED_NAME_LOWER}_sleepnumber_{BED_NAME_LOWER}"
            f"_{SLEEPER_L_NAME_LOWER}_bedtime"
        ).state
        == STATE_UNKNOWN
    )
