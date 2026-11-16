"""Test Chef iQ diagnostics."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.chef_iq.const import DOMAIN
from universalassistant.core import UniversalAssistant

from . import ADDRESS, CHEFIQ_STATUS_SERVICE_INFO, TITLE


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the diagnostics hold the latest advertisement, redacted."""
    # A user-edited title may hold personal information; it must not be exported.
    entry = MockConfigEntry(domain=DOMAIN, unique_id=ADDRESS, title="Backyard smoker")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, CHEFIQ_STATUS_SERVICE_INFO)
    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot(
        exclude=props("time")
    )


async def test_diagnostics_without_advertisement(
    hass: UniversalAssistant, hass_client: ClientSessionGenerator
) -> None:
    """Test the diagnostics of an entry whose probe has not been seen yet."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id=ADDRESS, title=TITLE)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == {
        "service_info": None
    }
