"""Test for diagnostics platform of the Bring! integration."""

from unittest.mock import AsyncMock

from bring_api import BringItemsResponse
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_load_fixture
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.bring.const import DOMAIN
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("mock_bring_client")
async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    bring_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    mock_bring_client: AsyncMock,
) -> None:
    """Test diagnostics."""
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
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, bring_config_entry)
        == snapshot
    )
