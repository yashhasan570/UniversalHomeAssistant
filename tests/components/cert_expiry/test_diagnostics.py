"""Tests for the Cert Expiry diagnostics."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.cert_expiry.const import DOMAIN
from universalassistant.components.cert_expiry.errors import ValidationFailure
from universalassistant.const import CONF_HOST, CONF_PORT, EVENT_HOMEASSISTANT_STARTED
from universalassistant.core import __HAC_KEEP__

from .const import HOST, PORT
from .helpers import future_timestamp, static_datetime


@pytest.mark.freeze_time(static_datetime())
async def test_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    # Create fake config entry: simulate "host = example.com, port = 443".
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: HOST, CONF_PORT: PORT},
        entry_id="test-entry",
        title=HOST,
        unique_id=f"{HOST}:{PORT}",
    )

    timestamp = future_timestamp(100)

    # patch network call and setup integration.
    with patch(
        "universalassistant.components.cert_expiry.coordinator.get_cert_expiry_timestamp",
        return_value=timestamp,
    ):
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
        await hass.async_block_till_done()

        assert (
            await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
        )


@pytest.mark.freeze_time(static_datetime())
async def test_config_entry_diagnostics_with_cert_error(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics with a certificate validation error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: HOST, CONF_PORT: PORT},
        entry_id="test-entry-error",
        title=HOST,
        unique_id=f"{HOST}:{PORT}",
    )

    with patch(
        "universalassistant.components.cert_expiry.coordinator.get_cert_expiry_timestamp",
        side_effect=ValidationFailure("certificate error for sensitive.example.com"),
    ):
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
        await hass.async_block_till_done()

        assert (
            await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
        )
