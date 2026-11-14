"""Tests for the Freebox diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from universalassistant.core import __HAC_KEEP__

from .common import setup_platform


@pytest.mark.usefixtures("router")
async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    entry = await setup_platform(hass, SENSOR_DOMAIN)

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
