"""Test the __HA_KEEP__ SkyConnect hardware platform."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.typing import WebSocketGenerator

from universalassistant.components.universalassistant_sky_connect.const import DOMAIN
from universalassistant.components.usb import DOMAIN as USB_DOMAIN
from universalassistant.const import EVENT_HOMEASSISTANT_STARTED
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

CONFIG_ENTRY_DATA = {
    "device": (
        "/dev/serial/by-id/"
        "usb-Nabu_Casa_SkyConnect_v1.0"
        "_9e2adbd75b8beb119fe564a0f320645d-if00-port0"
    ),
    "vid": "10C4",
    "pid": "EA60",
    "serial_number": "9e2adbd75b8beb119fe564a0f320645d",
    "manufacturer": "Nabu Casa",
    "product": "SkyConnect v1.0",
    "firmware": "ezsp",
}

CONFIG_ENTRY_DATA_2 = {
    "device": (
        "/dev/serial/by-id/"
        "usb-Nabu_Casa_Home_Assistant_Connect_ZBT-1"
        "_3c0ed67c628beb11b1cd64a0f320645d-if00-port0"
    ),
    "vid": "10C4",
    "pid": "EA60",
    "serial_number": "3c0ed67c628beb11b1cd64a0f320645d",
    "manufacturer": "Nabu Casa",
    "product": "__HA_KEEP__ Connect ZBT-1",
    "firmware": "ezsp",
}

CONFIG_ENTRY_DATA_BAD = {
    "device": (
        "/dev/serial/by-id/"
        "usb-Nabu_Casa_Home_Assistant_Connect_ZBT-1"
        "_a87b7d75b18beb119fe564a0f320645d-if00-port0"
    ),
}


async def test_hardware_info(
    hass: __HAC_KEEP__, hass_ws_client: WebSocketGenerator, addon_store_info
) -> None:
    """Test we can get the board info."""
    assert await async_setup_component(hass, USB_DOMAIN, {})
    hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)

    # Setup the config entry
    config_entry = MockConfigEntry(
        data=CONFIG_ENTRY_DATA,
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ SkyConnect",
        unique_id="unique_1",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)

    config_entry_2 = MockConfigEntry(
        data=CONFIG_ENTRY_DATA_2,
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ Connect ZBT-1",
        unique_id="unique_2",
        version=1,
        minor_version=2,
    )
    config_entry_2.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry_2.entry_id)

    config_entry_bad = MockConfigEntry(
        data=CONFIG_ENTRY_DATA_BAD,
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ Connect ZBT-1",
        unique_id="unique_3",
        version=1,
        minor_version=2,
    )
    config_entry_bad.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(config_entry_bad.entry_id)

    client = await hass_ws_client(hass)

    await client.send_json({"id": 1, "type": "hardware/info"})
    msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {
        "hardware": [
            {
                "board": None,
                "config_entries": [config_entry.entry_id],
                "dongle": {
                    "vid": "10C4",
                    "pid": "EA60",
                    "serial_number": "9e2adbd75b8beb119fe564a0f320645d",
                    "manufacturer": "Nabu Casa",
                    "description": "SkyConnect v1.0",
                },
                "name": "__HA_KEEP__ SkyConnect",
                "url": "https://support.nabucasa.com/hc/en-us/categories/24734620813469-Universal-Assistant-Connect-ZBT-1",
            },
            {
                "board": None,
                "config_entries": [config_entry_2.entry_id],
                "dongle": {
                    "vid": "10C4",
                    "pid": "EA60",
                    "serial_number": "3c0ed67c628beb11b1cd64a0f320645d",
                    "manufacturer": "Nabu Casa",
                    "description": "__HA_KEEP__ Connect ZBT-1",
                },
                "name": "__HA_KEEP__ Connect ZBT-1",
                "url": "https://support.nabucasa.com/hc/en-us/categories/24734620813469-Universal-Assistant-Connect-ZBT-1",
            },
            # Bad entry is skipped
        ]
    }
