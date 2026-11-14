"""Tests for the AVM Fritz!Box integration."""

from unittest.mock import Mock

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.diagnostics import REDACTED
from universalassistant.components.fritzbox.const import DOMAIN
from universalassistant.components.fritzbox.diagnostics import TO_REDACT
from universalassistant.const import CONF_DEVICES
from universalassistant.core import UniversalAssistant

from . import setup_config_entry
from .const import MOCK_CONFIG


async def test_entry_diagnostics(
    hass: UniversalAssistant, hass_client: ClientSessionGenerator, fritz: Mock
) -> None:
    """Test config entry diagnostics."""
    assert await setup_config_entry(hass, MOCK_CONFIG[DOMAIN][CONF_DEVICES][0])

    entries = hass.config_entries.async_entries(DOMAIN)
    entry_dict = entries[0].as_dict()
    for key in TO_REDACT:
        entry_dict["data"][key] = REDACTED

    result = await get_diagnostics_for_config_entry(hass, hass_client, entries[0])

    assert result == {"entry": entry_dict | {"discovery_keys": {}}, "data": {}}
