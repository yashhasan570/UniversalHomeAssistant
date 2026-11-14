"""Test nexia diagnostics."""

from nexia.home import NexiaHome
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__

from .conftest import setup_integration


async def test_diagnostics(
    hass: __HAC_KEEP__,
    patch_nexia_home: NexiaHome,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    entry = await setup_integration(hass, patch_nexia_home)

    diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)
    assert diag == snapshot
