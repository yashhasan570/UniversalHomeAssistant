"""Test the Netatmo diagnostics."""

from functools import partial
from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import paths

from universalassistant.components.netatmo import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from .common import fake_post_request


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    config_entry: MockConfigEntry,
) -> None:
    """Test config entry diagnostics."""
    with (
        patch(
            "universalassistant.components.netatmo.api.AsyncConfigEntryNetatmoAuth",
        ) as mock_auth,
        patch(
            "universalassistant.components.netatmo.async_get_config_entry_implementation",
        ),
        patch(
            "universalassistant.components.netatmo.webhook.webhook_generate_url",
        ),
    ):
        mock_auth.return_value.async_post_api_request.side_effect = partial(
            fake_post_request, hass
        )
        mock_auth.return_value.async_addwebhook.side_effect = AsyncMock()
        mock_auth.return_value.async_dropwebhook.side_effect = AsyncMock()
        assert await async_setup_component(hass, DOMAIN, {})

    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(
        exclude=paths(
            "info.data.token.expires_at",
            "info.entry_id",
            "info.created_at",
            "info.modified_at",
        )
    )
