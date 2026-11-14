"""Tests for the youless component."""

from pytest_universalassistant.common import (
    MockConfigEntry,
    async_load_json_array_fixture,
    async_load_json_object_fixture,
)
import requests_mock

from universalassistant.components.youless.const import DOMAIN
from universalassistant.const import CONF_DEVICE, CONF_HOST
from universalassistant.core import __HAC_KEEP__


async def init_component(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Check if the setup of the integration succeeds."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://1.1.1.1/d",
            json=await async_load_json_object_fixture(hass, "device.json", DOMAIN),
        )
        mock.get(
            "http://1.1.1.1/e",
            json=await async_load_json_array_fixture(hass, "enologic.json", DOMAIN),
            headers={"Content-Type": "application/json"},
        )
        mock.get(
            "http://1.1.1.1/f",
            json=await async_load_json_object_fixture(hass, "phase.json", DOMAIN),
            headers={"Content-Type": "application/json"},
        )

        entry = MockConfigEntry(
            domain=DOMAIN,
            title="localhost",
            data={CONF_HOST: "1.1.1.1", CONF_DEVICE: "localhost"},
        )
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
