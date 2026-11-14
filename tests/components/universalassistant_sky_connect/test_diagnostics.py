"""Tests for the __HA_KEEP__ SkyConnect diagnostics data."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.universalassistant_hardware.util import (
    ApplicationType,
    FirmwareInfo,
    OwningAddon,
    OwningIntegration,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

from .common import USB_DATA_ZBT1


async def test_diagnostics_for_config_entry(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for config entry."""
    await async_setup_component(hass, "universalassistant", {})

    zha_config_entry = MockConfigEntry(domain="zha")
    zha_config_entry.add_to_hass(hass)

    config_entry = MockConfigEntry(
        domain="universalassistant_sky_connect",
        unique_id=USB_DATA_ZBT1.serial_number,
        data={
            "firmware": "ezsp",
            "firmware_version": "7.4.4.0 build 0",
            "device": USB_DATA_ZBT1.device,
            "manufacturer": USB_DATA_ZBT1.manufacturer,
            "pid": USB_DATA_ZBT1.pid,
            "product": USB_DATA_ZBT1.description,
            "serial_number": USB_DATA_ZBT1.serial_number,
            "vid": USB_DATA_ZBT1.vid,
        },
        version=1,
        minor_version=5,
    )
    config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    with patch(
        "universalassistant.components.universalassistant_sky_connect.diagnostics.guess_hardware_owners",
        return_value=[
            FirmwareInfo(
                device=USB_DATA_ZBT1.device,
                firmware_type=ApplicationType.EZSP,
                firmware_version="7.4.4.0 build 0",
                source="zha",
                owners=[OwningIntegration(config_entry_id=zha_config_entry.entry_id)],
            ),
            FirmwareInfo(
                device=USB_DATA_ZBT1.device,
                firmware_type=ApplicationType.EZSP,
                firmware_version=None,
                source="zigbee2mqtt (core_zigbee2mqtt)",
                owners=[OwningAddon(slug="core_zigbee2mqtt")],
            ),
        ],
    ):
        diagnostics_data = await get_diagnostics_for_config_entry(
            hass, hass_client, config_entry
        )

    assert diagnostics_data == snapshot
