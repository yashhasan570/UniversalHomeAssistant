"""Tests for Plex buttons."""

from datetime import timedelta
from unittest.mock import patch

from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.plex.const import DEBOUNCE_TIMEOUT
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.util import dt as dt_util


async def test_scan_clients_button_schedule(
    hass: __HAC_KEEP__, setup_plex_server
) -> None:
    """Test scan_clients button scheduled update."""
    with patch(
        "universalassistant.components.plex.server.PlexServer._async_update_platforms"
    ) as mock_scan_clients:
        await setup_plex_server()
        mock_scan_clients.reset_mock()

        async_fire_time_changed(
            hass,
            dt_util.utcnow() + timedelta(seconds=DEBOUNCE_TIMEOUT),
        )

        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                CommonServiceArgument.ENTITY_ID: "button.plex_server_1_scan_clients",
            },
            True,
        )
        await hass.async_block_till_done()

    assert mock_scan_clients.called
