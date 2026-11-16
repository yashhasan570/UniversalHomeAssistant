"""Tests for Tradfri diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from pytradfri.device import Device

from universalassistant.core import UniversalAssistant

from .common import setup_integration


@pytest.mark.parametrize("device", ["air_purifier"], indirect=True)
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    device: Device,
) -> None:
    """Test diagnostics for config entry."""
    config_entry = await setup_integration(hass)

    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert isinstance(result, dict)
    assert result["gateway_version"] == "1.2.1234"
    assert result["device_data"] == ["STARKVIND Air purifier"]
