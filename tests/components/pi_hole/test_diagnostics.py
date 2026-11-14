"""Test pi_hole component."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components import pi_hole
from universalassistant.core import __HAC_KEEP__

from . import CONFIG_DATA_DEFAULTS, _create_mocked_hole, _patch_init_hole


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Tests diagnostics."""
    mocked_hole = _create_mocked_hole(api_version=5)
    config_entry = {**CONFIG_DATA_DEFAULTS, "api_version": 5}
    entry = MockConfigEntry(
        domain=pi_hole.DOMAIN, data=config_entry, entry_id="pi_hole_mock_entry"
    )
    entry.add_to_hass(hass)
    with _patch_init_hole(mocked_hole):
        assert await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot(
        exclude=props("created_at", "modified_at")
    )
