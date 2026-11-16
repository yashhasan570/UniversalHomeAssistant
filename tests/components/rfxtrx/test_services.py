"""The tests for the Rfxtrx services."""

import probatio
import pytest

from universalassistant.components.rfxtrx import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.setup import async_setup_component


async def test_send_invalid_event(hass: UniversalAssistant) -> None:
    """Test send of an invalid event fails validation."""
    await async_setup_component(hass, DOMAIN, {})

    with pytest.raises(probatio.Invalid):
        await hass.services.async_call(
            DOMAIN, "send", {"event": "invalid"}, blocking=True
        )


async def test_send_not_connected(hass: UniversalAssistant) -> None:
    """Test send fails if there is no active RFXtrx connection."""
    await async_setup_component(hass, DOMAIN, {})

    with pytest.raises(UniversalAssistantError, match="RFXtrx is not connected"):
        await hass.services.async_call(
            DOMAIN, "send", {"event": "0a520802060101ff0f0269"}, blocking=True
        )
