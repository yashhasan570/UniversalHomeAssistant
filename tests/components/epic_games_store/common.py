"""Common methods used across tests for Epic Games Store."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.epic_games_store.const import DOMAIN
from universalassistant.const import CONF_COUNTRY, CONF_LANGUAGE
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

from .const import MOCK_COUNTRY, MOCK_LANGUAGE


async def setup_platform(hass: __HAC_KEEP__, platform: str) -> MockConfigEntry:
    """Set up the Epic Games Store platform."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_LANGUAGE: MOCK_LANGUAGE,
            CONF_COUNTRY: MOCK_COUNTRY,
        },
        unique_id=f"freegames-{MOCK_LANGUAGE}-{MOCK_COUNTRY}",
    )
    mock_entry.add_to_hass(hass)

    with patch("universalassistant.components.epic_games_store.PLATFORMS", [platform]):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return mock_entry
