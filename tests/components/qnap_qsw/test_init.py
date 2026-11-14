"""Define tests for the QNAP QSW init."""

from unittest.mock import patch

from aioqsw.exceptions import APIError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.qnap_qsw.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from .util import CONFIG


async def test_firmware_check_error(hass: __HAC_KEEP__) -> None:
    """Test firmware update check error."""

    config_entry = MockConfigEntry(
        domain=DOMAIN, unique_id="qsw_unique_id", data=CONFIG
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.check_firmware",
            side_effect=APIError,
        ),
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.validate",
            return_value=None,
        ),
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.update",
            return_value=None,
        ),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED


async def test_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test unload."""

    config_entry = MockConfigEntry(
        domain=DOMAIN, unique_id="qsw_unique_id", data=CONFIG
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.check_firmware",
            return_value=None,
        ),
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.validate",
            return_value=None,
        ),
        patch(
            "universalassistant.components.qnap_qsw.QnapQswApi.update",
            return_value=None,
        ),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.NOT_LOADED
