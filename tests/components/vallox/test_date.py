"""Tests for Vallox date platform."""

from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.date import DOMAIN as DATE_DOMAIN, SERVICE_SET_VALUE
from universalassistant.const import ATTR_DATE, ATTR_ENTITY_ID, STATE_UNKNOWN, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration

DATE_ENTITY_ID = "date.vallox_filter_change_date"


@pytest.mark.usefixtures("mock_vallox_client")
async def test_all_entities(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the date entity."""
    with patch("universalassistant.components.vallox.PLATFORMS", [Platform.DATE]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize("metrics", [{"A_CYC_FILTER_CHANGED_DAY": None}])
async def test_filter_change_date_missing(hass: __HAC_KEEP__) -> None:
    """Test a filter change date the unit does not report."""
    state = hass.states.get(DATE_ENTITY_ID)
    assert state
    assert state.state == STATE_UNKNOWN


@pytest.mark.usefixtures("init_integration")
async def test_set_filter_change_date(
    hass: __HAC_KEEP__, mock_vallox_client: AsyncMock
) -> None:
    """Test setting the filter change date."""
    await hass.services.async_call(
        DATE_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: DATE_ENTITY_ID, ATTR_DATE: "2024-02-25"},
        blocking=True,
    )

    mock_vallox_client.set_filter_change_date.assert_called_once_with(date(2024, 2, 25))
    # One fetch at setup, and one refresh after the change.
    assert mock_vallox_client.fetch_metric_data.call_count == 2
