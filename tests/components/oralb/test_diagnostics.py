"""Tests for the diagnostics data provided by the Oral-B integration."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.oralb.const import DOMAIN
from universalassistant.core import UniversalAssistant

from . import ORALB_IO_SERIES_4_SERVICE_INFO


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN, unique_id=ORALB_IO_SERIES_4_SERVICE_INFO.address
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, ORALB_IO_SERIES_4_SERVICE_INFO)
    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot


async def test_diagnostics_no_advertisement(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics before any advertisement has been received."""
    entry = MockConfigEntry(
        domain=DOMAIN, unique_id=ORALB_IO_SERIES_4_SERVICE_INFO.address
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
