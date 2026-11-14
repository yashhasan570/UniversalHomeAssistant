"""Test AirNow diagnostics."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import UniversalAssistant


@pytest.mark.usefixtures("setup_airnow")
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""

    # Fake LocalTimeZoneInfo
    with patch(
        "universalassistant.util.dt.async_get_time_zone",
        return_value="PST",
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        assert await get_diagnostics_for_config_entry(
            hass, hass_client, config_entry
        ) == snapshot(exclude=props("created_at", "modified_at"))
