"""Test the Downloader config flow."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.downloader.const import CONF_DOWNLOAD_DIR, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

CONFIG = {CONF_DOWNLOAD_DIR: "download_dir"}


async def test_user_form(hass: UniversalAssistant) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=CONFIG,
    )
    assert result["type"] is FlowResultType.FORM

    with patch("os.path.isdir", return_value=False):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONFIG,
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {"base": "directory_does_not_exist"}

    with (
        patch(
            "universalassistant.components.downloader.async_setup_entry", return_value=None
        ),
        patch(
            "os.path.isdir",
            return_value=True,
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONFIG,
        )
        await hass.async_block_till_done()
        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "Downloader"
        assert result["data"] == {"download_dir": "download_dir"}


@pytest.mark.parametrize("source", [SOURCE_USER])
async def test_single_instance_allowed(
    hass: UniversalAssistant,
    source: str,
) -> None:
    """Test we abort if already setup."""
    mock_config_entry = MockConfigEntry(domain=DOMAIN)
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": source}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
