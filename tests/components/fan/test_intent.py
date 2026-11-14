"""Intent tests for the fan platform."""

from pytest_universalassistant.common import async_mock_service

from universalassistant.components.fan import (
    ATTR_PERCENTAGE,
    DOMAIN,
    SERVICE_TURN_ON,
    intent as fan_intent,
)
from universalassistant.const import STATE_OFF
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import intent


async def test_set_speed_intent(hass: __HAC_KEEP__) -> None:
    """Test set speed intent for fans."""
    await fan_intent.async_setup_intents(hass)

    entity_id = f"{DOMAIN}.test_fan"
    hass.states.async_set(entity_id, STATE_OFF)
    calls = async_mock_service(hass, DOMAIN, SERVICE_TURN_ON)

    response = await intent.async_handle(
        hass,
        "test",
        fan_intent.INTENT_FAN_SET_SPEED,
        {"name": {"value": "test fan"}, ATTR_PERCENTAGE: {"value": 50}},
    )
    await hass.async_block_till_done()

    assert response.response_type is intent.IntentResponseType.ACTION_DONE
    assert len(calls) == 1
    call = calls[0]
    assert call.domain == DOMAIN
    assert call.service == SERVICE_TURN_ON
    assert call.data == {"entity_id": entity_id, "percentage": 50}
