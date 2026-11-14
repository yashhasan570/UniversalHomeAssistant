"""Test the Rhasspy config flow."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.rhasspy.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with patch(
        "universalassistant.components.rhasspy.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Rhasspy"
    assert result2["data"] == {}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_single_entry(hass: __HAC_KEEP__) -> None:
    """Test we only allow single entry."""
    MockConfigEntry(domain=DOMAIN).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
