"""Tests for the diagnostics data provided by the easyEnergy integration."""

from unittest.mock import MagicMock

from easyenergy import EasyEnergyNoDataError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.universalassistant import (
    DOMAIN as HOMEASSISTANT_DOMAIN,
    SERVICE_UPDATE_ENTITY,
)
from universalassistant.const import ATTR_ENTITY_ID
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.mark.freeze_time("2026-04-19 13:00:00+00:00")
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )


@pytest.mark.freeze_time("2026-04-19 13:00:00+00:00")
async def test_diagnostics_no_gas_today(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_easyenergy: MagicMock,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics, no gas sensors available."""
    await async_setup_component(hass, HOMEASSISTANT_DOMAIN, {})
    mock_easyenergy.gas_prices.side_effect = EasyEnergyNoDataError

    await hass.services.async_call(
        HOMEASSISTANT_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["sensor.gas_market_price_current_hour"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )
