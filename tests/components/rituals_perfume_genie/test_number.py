"""Tests for the Rituals Perfume Genie number platform."""

import pytest
from ritualsgenie import RitualsGenieConnectionError

from universalassistant.components.universalassistant import (
    DOMAIN as HOMEASSISTANT_DOMAIN,
    SERVICE_UPDATE_ENTITY,
)
from universalassistant.components.number import (
    ATTR_MAX,
    ATTR_MIN,
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import ATTR_ENTITY_ID, CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import entity_registry as er
from universalassistant.setup import async_setup_component

from .common import (
    init_integration,
    mock_config_entry,
    mock_diffuser,
    mock_diffuser_v1_battery_cartridge,
)


async def test_number_entity(
    hass: __HAC_KEEP__, entity_registry: er.EntityRegistry
) -> None:
    """Test the creation and values of the diffuser number entity."""
    config_entry = mock_config_entry(unique_id="number_test")
    diffuser = mock_diffuser(hublot="lot123", perfume_amount=2)
    await init_integration(hass, config_entry, [diffuser])

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == str(diffuser.perfume_amount)
    assert state.attributes[ATTR_MIN] == 1
    assert state.attributes[ATTR_MAX] == 3

    entry = entity_registry.async_get("number.genie_perfume_amount")
    assert entry
    assert entry.unique_id == f"{diffuser.hublot}-perfume_amount"


async def test_set_number_value(hass: __HAC_KEEP__) -> None:
    """Test setting the diffuser number entity value."""
    config_entry = mock_config_entry(unique_id="number_set_value_test")
    diffuser = mock_diffuser_v1_battery_cartridge()
    client = await init_integration(hass, config_entry, [diffuser])
    await async_setup_component(hass, HOMEASSISTANT_DOMAIN, {})

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "2"

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: "number.genie_perfume_amount",
            NumberServiceArgument.VALUE: 1,
        },
        blocking=True,
    )

    client.set_perfume_amount.assert_awaited_once_with(diffuser.hub_hash, 1)

    # The new value shows right away, without waiting for the next update.
    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "1"

    diffuser.perfume_amount = 1
    await hass.services.async_call(
        HOMEASSISTANT_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["number.genie_perfume_amount"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "1"


async def test_set_number_value_out_of_range(hass: __HAC_KEEP__) -> None:
    """Test setting the diffuser number entity value out of range."""
    config_entry = mock_config_entry(unique_id="number_set_value_out_of_range_test")
    diffuser = mock_diffuser(hublot="lot123", perfume_amount=2)
    await init_integration(hass, config_entry, [diffuser])
    await async_setup_component(hass, HOMEASSISTANT_DOMAIN, {})

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "2"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.genie_perfume_amount",
                NumberServiceArgument.VALUE: 4,
            },
            blocking=True,
        )
    await hass.services.async_call(
        HOMEASSISTANT_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["number.genie_perfume_amount"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "2"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.genie_perfume_amount",
                NumberServiceArgument.VALUE: 0,
            },
            blocking=True,
        )
    await hass.services.async_call(
        HOMEASSISTANT_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["number.genie_perfume_amount"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "2"


async def test_set_number_value_to_float(hass: __HAC_KEEP__) -> None:
    """Test setting the diffuser number entity value to a float."""
    config_entry = mock_config_entry(unique_id="number_set_value_to_float_test")
    diffuser = mock_diffuser(hublot="lot123", perfume_amount=3)
    await init_integration(hass, config_entry, [diffuser])
    await async_setup_component(hass, HOMEASSISTANT_DOMAIN, {})

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "3"

    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.genie_perfume_amount",
                NumberServiceArgument.VALUE: 1.5,
            },
            blocking=True,
        )
    assert exc_info.value.translation_key == "perfume_amount_not_whole"
    await hass.services.async_call(
        HOMEASSISTANT_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["number.genie_perfume_amount"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "3"


async def test_number_action_error(hass: __HAC_KEEP__) -> None:
    """Test a failing change of the perfume amount raises a translated error."""
    config_entry = mock_config_entry(unique_id="id_123_number_action_error")
    client = await init_integration(hass, config_entry, [mock_diffuser("lot123")])
    client.set_perfume_amount.side_effect = RitualsGenieConnectionError

    with pytest.raises(__HAC_KEEP__Error) as exc_info:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.genie_perfume_amount",
                NumberServiceArgument.VALUE: 1,
            },
            blocking=True,
        )

    assert exc_info.value.translation_key == "communication_error"
    state = hass.states.get("number.genie_perfume_amount")
    assert state
    assert state.state == "2"
