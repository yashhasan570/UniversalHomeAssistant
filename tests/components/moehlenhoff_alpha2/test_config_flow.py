"""Test the moehlenhoff_alpha2 config flow."""

from functools import partialmethod
from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.moehlenhoff_alpha2.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from . import MOCK_BASE_HOST, mock_update_data


async def _assert_recovers(hass: __HAC_KEEP__, flow_id: str) -> None:
    """Assert the flow creates an entry once the device answers."""
    with (
        patch(
            "universalassistant.components.moehlenhoff_alpha2.config_flow.Alpha2Base.update_data",
            partialmethod(mock_update_data, hass),
        ),
        patch(
            "universalassistant.components.moehlenhoff_alpha2.async_setup_entry",
            return_value=None,
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            flow_id=flow_id,
            user_input={"host": MOCK_BASE_HOST},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_form(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]

    with (
        patch(
            "universalassistant.components.moehlenhoff_alpha2.config_flow.Alpha2Base.update_data",
            partialmethod(mock_update_data, hass),
        ),
        patch(
            "universalassistant.components.moehlenhoff_alpha2.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=result["flow_id"],
            user_input={"host": MOCK_BASE_HOST},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Alpha2Test"
    assert result2["data"] == {"host": MOCK_BASE_HOST}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_duplicate_error(hass: __HAC_KEEP__) -> None:
    """Test that errors are shown when duplicates are added."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"host": MOCK_BASE_HOST},
        source=config_entries.SOURCE_USER,
    )
    config_entry.add_to_hass(hass)

    assert config_entry.data["host"] == MOCK_BASE_HOST

    with patch(
        "moehlenhoff_alpha2.Alpha2Base.update_data",
        partialmethod(mock_update_data, hass),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"host": MOCK_BASE_HOST},
        )
        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == "already_configured"


async def test_form_cannot_connect_error(hass: __HAC_KEEP__) -> None:
    """Test connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    with patch("moehlenhoff_alpha2.Alpha2Base.update_data", side_effect=TimeoutError):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=result["flow_id"],
            user_input={"host": MOCK_BASE_HOST},
        )

        assert result2["type"] is FlowResultType.FORM
        assert result2["errors"] == {"base": "cannot_connect"}

    await _assert_recovers(hass, result["flow_id"])


async def test_form_unexpected_error(hass: __HAC_KEEP__) -> None:
    """Test unexpected error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    with patch("moehlenhoff_alpha2.Alpha2Base.update_data", side_effect=Exception):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=result["flow_id"],
            user_input={"host": MOCK_BASE_HOST},
        )

        assert result2["type"] is FlowResultType.FORM
        assert result2["errors"] == {"base": "unknown"}

    await _assert_recovers(hass, result["flow_id"])
