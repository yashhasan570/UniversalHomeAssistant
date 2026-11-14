"""Test Prosegur diagnostics."""

from unittest.mock import patch

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.core import UniversalAssistant


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    init_integration,
    mock_install,
) -> None:
    """Test generating diagnostics for a config entry."""

    with patch(
        "pyprosegur.installation.Installation.retrieve", return_value=mock_install
    ):
        diag = await get_diagnostics_for_config_entry(
            hass, hass_client, init_integration
        )

        assert diag == {
            "installation": {"contract": "1234abcd"},
            "activity": {"event": "armed"},
        }
