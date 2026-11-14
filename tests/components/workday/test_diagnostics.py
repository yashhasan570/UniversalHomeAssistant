"""Test Workday diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import __HAC_KEEP__

from . import TEST_CONFIG_ADD_REMOVE_DATE_RANGE, init_integration


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    entry = await init_integration(hass, TEST_CONFIG_ADD_REMOVE_DATE_RANGE)

    diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert diag == snapshot(
        exclude=props("full_features", "created_at", "modified_at"),
    )
