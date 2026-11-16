"""Test the Rainforest Eagle diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.diagnostics import REDACTED
from universalassistant.components.rainforest_eagle.const import (
    CONF_CLOUD_ID,
    CONF_INSTALL_CODE,
)
from universalassistant.core import UniversalAssistant

from . import MOCK_200_RESPONSE_WITHOUT_PRICE


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    setup_rainforest_200,
    config_entry_200,
) -> None:
    """Test config entry diagnostics."""
    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry_200)

    config_entry_dict = config_entry_200.as_dict()
    config_entry_dict["data"][CONF_INSTALL_CODE] = REDACTED
    config_entry_dict["data"][CONF_CLOUD_ID] = REDACTED

    assert result == {
        "config_entry": config_entry_dict | {"discovery_keys": {}},
        "data": {
            var["Name"]: var["Value"]
            for var in MOCK_200_RESPONSE_WITHOUT_PRICE.values()
        },
    }
