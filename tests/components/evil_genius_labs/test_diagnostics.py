"""Test evil genius labs diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.diagnostics import REDACTED
from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize("platforms", [[]])
async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    setup_evil_genius_labs,
    config_entry,
    all_fixture,
    info_fixture,
) -> None:
    """Test config entry diagnostics."""
    assert await get_diagnostics_for_config_entry(hass, hass_client, config_entry) == {
        "info": {
            **info_fixture,
            "wiFiSsidDefault": REDACTED,
            "wiFiSSID": REDACTED,
        },
        "all": all_fixture,
    }
