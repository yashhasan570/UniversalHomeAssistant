"""Tests for the local_ip config_flow."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.local_ip.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_config_flow(hass: __HAC_KEEP__) -> None:
    """Test we can finish a config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] is FlowResultType.CREATE_ENTRY

    await hass.async_block_till_done()
    state = hass.states.get(f"sensor.{DOMAIN}")
    assert state


async def test_already_setup(hass: __HAC_KEEP__) -> None:
    """Test we abort if already setup."""
    MockConfigEntry(
        domain=DOMAIN,
        data={},
    ).add_to_hass(hass)

    # Should fail, same NAME
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
