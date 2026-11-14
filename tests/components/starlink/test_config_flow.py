"""Test the Starlink config flow."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.starlink.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_IP_ADDRESS
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from .patchers import DEVICE_FOUND_PATCHER, NO_DEVICE_PATCHER, SETUP_ENTRY_PATCHER


async def test_flow_user_fails_can_succeed(hass: __HAC_KEEP__) -> None:
    """Test user flow can succeed after failure when Starlink is available."""
    user_input = {CONF_IP_ADDRESS: "192.168.100.1:9200"}

    with NO_DEVICE_PATCHER, SETUP_ENTRY_PATCHER:
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
        )
        await hass.async_block_till_done()
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=user_input,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert result["errors"]

    with DEVICE_FOUND_PATCHER, SETUP_ENTRY_PATCHER:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=user_input,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == user_input


async def test_flow_user_success(hass: __HAC_KEEP__) -> None:
    """Test user initialized flow succeeds when Starlink is available."""
    user_input = {CONF_IP_ADDRESS: "192.168.100.1:9200"}

    with DEVICE_FOUND_PATCHER, SETUP_ENTRY_PATCHER:
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
        )
        await hass.async_block_till_done()
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=user_input,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == user_input
    assert result["result"].unique_id == "some-valid-id"


async def test_flow_user_duplicate_abort(hass: __HAC_KEEP__) -> None:
    """Test user initialized flow aborts when Starlink is already configured."""
    user_input = {CONF_IP_ADDRESS: "192.168.100.1:9200"}

    entry = MockConfigEntry(
        domain=DOMAIN,
        data=user_input,
        unique_id="some-valid-id",
        state=config_entries.ConfigEntryState.LOADED,
    )
    entry.add_to_hass(hass)

    with DEVICE_FOUND_PATCHER, SETUP_ENTRY_PATCHER:
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
        )
        await hass.async_block_till_done()
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=user_input,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
