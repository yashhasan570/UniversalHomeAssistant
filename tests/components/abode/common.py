"""Common methods used across tests for Abode."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.abode import DOMAIN
from universalassistant.components.abode.const import CONF_POLLING
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def setup_platform(hass: UniversalAssistant, platform: str) -> MockConfigEntry:
    """Set up the Abode platform."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "user@email.com",
            CONF_PASSWORD: "password",
            CONF_POLLING: False,
        },
    )
    mock_entry.add_to_hass(hass)

    with (
        patch("universalassistant.components.abode.PLATFORMS", [platform]),
        patch("jaraco.abode.event_controller.sio"),
    ):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return mock_entry
