"""Test the Tado component diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.tado.const import DOMAIN
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("init_integration")
async def test_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test if get_config_entry_diagnostics returns the correct data."""
    config_entry: MockConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]
    diagnostics = await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    )
    assert diagnostics == snapshot(exclude=props("created_at", "modified_at"))
