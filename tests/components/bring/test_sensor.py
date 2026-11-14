"""Test for sensor platform of the Bring! integration."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

from bring_api import BringItemsResponse
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_load_fixture,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.bring.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def sensor_only() -> Generator[None]:
    """Enable only the sensor platform."""
    with patch(
        "universalassistant.components.bring.PLATFORMS",
        [Platform.SENSOR],
    ):
        yield


async def test_setup(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_bring_client: AsyncMock,
) -> None:
    """Snapshot test states of sensor platform."""

    mock_bring_client.get_list.side_effect = [
        BringItemsResponse.from_json(
            await async_load_fixture(hass, "items.json", DOMAIN)
        ),
        BringItemsResponse.from_json(
            await async_load_fixture(hass, "items2.json", DOMAIN)
        ),
    ]
    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(
        hass, entity_registry, snapshot, bring_config_entry.entry_id
    )


@pytest.mark.parametrize(
    ("fixture", "entity_state"),
    [
        ("items_invitation", "invitation"),
        ("items_shared", "shared"),
        ("items", "registered"),
    ],
)
async def test_list_access_states(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    mock_bring_client: AsyncMock,
    fixture: str,
    entity_state: str,
) -> None:
    """Snapshot test states of list access sensor."""

    mock_bring_client.get_list.return_value = BringItemsResponse.from_json(
        await async_load_fixture(hass, f"{fixture}.json", DOMAIN)
    )
    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    assert (state := hass.states.get("sensor.einkauf_list_access"))
    assert state.state == entity_state
