"""Tests for the Stookwijzer services."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.stookwijzer.const import DOMAIN
from universalassistant.components.stookwijzer.services import StookwijzerService
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ServiceValidationError
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("init_integration")
async def test_service_get_forecast(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the Stookwijzer forecast service."""

    assert snapshot == await hass.services.async_call(
        DOMAIN,
        StookwijzerService.GET_FORECAST,
        {CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id},
        blocking=True,
        return_response=True,
    )


@pytest.mark.usefixtures("init_integration")
async def test_service_entry_not_loaded(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test error handling when entry is not loaded."""
    mock_config_entry2 = MockConfigEntry(domain=DOMAIN)
    mock_config_entry2.add_to_hass(hass)

    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            StookwijzerService.GET_FORECAST,
            {CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry2.entry_id},
            blocking=True,
            return_response=True,
        )
    assert err.value.translation_key == "service_config_entry_not_loaded"


@pytest.mark.usefixtures("init_integration")
async def test_service_integration_not_found(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test error handling when integration not in registry."""
    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            StookwijzerService.GET_FORECAST,
            {CommonServiceArgument.CONFIG_ENTRY_ID: "bad-config_id"},
            blocking=True,
            return_response=True,
        )
    assert err.value.translation_key == "service_config_entry_not_found"
