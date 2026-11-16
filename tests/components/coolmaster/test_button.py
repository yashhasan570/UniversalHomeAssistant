"""The test for the Coolmaster button platform."""

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CommonServiceArgument
from universalassistant.core import UniversalAssistant


async def test_button(
    hass: UniversalAssistant,
    load_int: ConfigEntry,
) -> None:
    """Test the Coolmaster button."""
    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "on"

    button = hass.states.get("button.l1_101_reset_filter")
    assert button is not None
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            CommonServiceArgument.ENTITY_ID: button.entity_id,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "off"
