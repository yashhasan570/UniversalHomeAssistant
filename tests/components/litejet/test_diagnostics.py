"""The tests for the litejet component."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.core import __HAC_KEEP__

from . import async_init_integration


async def test_diagnostics(
    hass: __HAC_KEEP__, hass_client: ClientSessionGenerator, mock_litejet
) -> None:
    """Test getting the LiteJet diagnostics."""

    config_entry = await async_init_integration(hass)

    diag = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert diag == {
        "model": "MockJet",
        "loads": [1, 2],
        "button_switches": [1, 2],
        "scenes": [1, 2],
        "connected": True,
    }
