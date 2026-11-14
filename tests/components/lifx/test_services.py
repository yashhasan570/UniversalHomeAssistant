"""Tests for the LIFX services."""

from unittest.mock import patch

from lifx import LifxTimeoutError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.lifx import DOMAIN
from universalassistant.components.lifx.const import CONF_SERIAL, LIFXService
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import ATTR_ENTITY_ID, CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ServiceValidationError
from universalassistant.setup import async_setup_component

from . import IP_ADDRESS, SERIAL
from .helpers import create_mock_hev_light

SERVICES = (
    LIFXService.EFFECT_COLORLOOP,
    LIFXService.EFFECT_FLAME,
    LIFXService.EFFECT_MORPH,
    LIFXService.EFFECT_MOVE,
    LIFXService.EFFECT_PULSE,
    LIFXService.EFFECT_SKY,
    LIFXService.EFFECT_STOP,
    LIFXService.PAINT_THEME,
)


@pytest.mark.usefixtures("mock_discovery")
async def test_services_registered_without_entry(hass: __HAC_KEEP__) -> None:
    """Test all actions are registered during component setup."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()

    for service in (*SERVICES, "set_state", "set_hev_cycle_state"):
        assert hass.services.has_service(DOMAIN, service)


@pytest.mark.usefixtures("mock_discovery")
async def test_service_without_loaded_entry_raises(hass: __HAC_KEEP__) -> None:
    """Test the effect actions raise when no config entry is loaded."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()

    # Every effect action shares one handler
    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            LIFXService.EFFECT_PULSE,
            {ATTR_ENTITY_ID: "light.test"},
            blocking=True,
        )

    assert err.value.translation_domain == DOMAIN
    assert err.value.translation_key == "not_loaded"
    assert "LIFX is not loaded" in str(err.value)


@pytest.mark.parametrize("service", ["set_state", "set_hev_cycle_state"])
@pytest.mark.usefixtures("mock_discovery")
async def test_entity_action_does_not_control_device_after_failed_setup(
    hass: __HAC_KEEP__, service: str
) -> None:
    """Test registered entity actions cannot command a device that failed setup."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        version=2,
        data={CONF_HOST: IP_ADDRESS, CONF_SERIAL: SERIAL},
        unique_id=SERIAL,
    )
    entry.add_to_hass(hass)
    device = create_mock_hev_light()
    device.refresh_state.side_effect = LifxTimeoutError("timed out")
    with patch("universalassistant.components.lifx.Device.connect", return_value=device):
        assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert hass.services.has_service(DOMAIN, service)

    await hass.services.async_call(
        DOMAIN,
        service,
        {ATTR_ENTITY_ID: "light.my_group_my_bulb", "power": True},
        blocking=True,
    )

    device.set_power.assert_not_called()
    device.set_color.assert_not_called()
    device.set_hev_cycle.assert_not_called()
