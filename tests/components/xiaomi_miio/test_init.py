"""Tests for the Xiaomi Miio integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.xiaomi_miio.const import CONF_FLOW_TYPE, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_DEVICE, CONF_HOST, CONF_MAC, CONF_MODEL, CONF_TOKEN
from universalassistant.core import UniversalAssistant


async def test_setup_unsupported_model(hass: UniversalAssistant) -> None:
    """Test setup fails for an unsupported device model."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="123456",
        title="Unsupported device",
        data={
            CONF_FLOW_TYPE: CONF_DEVICE,
            CONF_HOST: "192.168.1.100",
            CONF_TOKEN: "12345678901234567890123456789012",
            CONF_MODEL: "unsupported.model.v1",
            CONF_MAC: "AA:BB:CC:DD:EE:FF",
        },
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Unsupported Xiaomi Miio device model: unsupported.model.v1"
