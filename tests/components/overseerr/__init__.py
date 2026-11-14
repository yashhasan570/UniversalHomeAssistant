"""Tests for the Overseerr integration."""

from typing import Any
from urllib.parse import urlparse

from aiohttp.test_utils import TestClient
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.webhook import async_generate_url
from universalassistant.core import __HAC_KEEP__

from .const import WEBHOOK_ID


async def setup_integration(hass: __HAC_KEEP__, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


async def call_webhook(
    hass: __HAC_KEEP__, data: dict[str, Any], client: TestClient
) -> None:
    """Call the webhook."""
    webhook_url = async_generate_url(hass, WEBHOOK_ID)

    resp = await client.post(
        urlparse(webhook_url).path,
        json=data,
    )

    # Wait for remaining tasks to complete.
    await hass.async_block_till_done()

    data = await resp.json()
    resp.close()
