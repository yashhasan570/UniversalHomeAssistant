"""Tests for the Enphase Envoy integration."""

from datetime import timedelta

from jwt import encode
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util

TOKEN_SIGNING_KEY = "envoy-test-signing-key-0123456789"


async def setup_integration(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    expected_state: ConfigEntryState = ConfigEntryState.LOADED,
) -> None:
    """Fixture for setting up the component and testing expected state."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert config_entry.state is expected_state


def envoy_token(days_to_expiry: int = 365) -> str:
    """Build envoy token with specified days to expiration."""
    return encode(
        payload={
            "name": "envoy",
            "exp": (dt_util.utcnow() + timedelta(days=days_to_expiry)).timestamp(),
        },
        key=TOKEN_SIGNING_KEY,
        algorithm="HS256",
    )
