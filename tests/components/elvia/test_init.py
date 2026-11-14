"""Tests for the Elvia integration setup."""

from unittest.mock import patch

from elvia import error as ElviaError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.elvia.const import CONF_METERING_POINT_ID, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_API_TOKEN
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("recorder_mock")
async def test_setup_import_failed(hass: __HAC_KEEP__) -> None:
    """Test setup fails when the initial import of meter values fails."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_TOKEN: "token", CONF_METERING_POINT_ID: "1234"},
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.elvia.importer.ElviaImporter.import_meter_values",
        side_effect=ElviaError.ElviaException("Boom"),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Failed to import meter values from Elvia"
