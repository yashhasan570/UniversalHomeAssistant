"""Tests for the LG webOS TV integration."""

from typing import Any

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.webostv.const import DOMAIN
from universalassistant.const import CONF_CLIENT_SECRET, CONF_HOST
from universalassistant.core import __HAC_KEEP__

from .const import CLIENT_KEY, FAKE_UUID, HOST, TV_NAME


async def setup_webostv(
    hass: __HAC_KEEP__,
    unique_id: str | None = FAKE_UUID,
    options: dict[str, Any] | None = None,
) -> MockConfigEntry:
    """Initialize webostv and media_player for tests."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: HOST,
            CONF_CLIENT_SECRET: CLIENT_KEY,
        },
        options=options or {},
        title=TV_NAME,
        unique_id=unique_id,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry
