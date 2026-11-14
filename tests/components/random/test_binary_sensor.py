"""The test for the Random binary sensor platform."""

from unittest.mock import patch

from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_random_binary_sensor_on(hass: __HAC_KEEP__) -> None:
    """Test the Random binary sensor."""
    config = {"binary_sensor": {"platform": "random", "name": "test"}}

    with patch(
        "universalassistant.components.random.binary_sensor.getrandbits",
        return_value=1,
    ):
        assert await async_setup_component(
            hass,
            "binary_sensor",
            config,
        )
        await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.test")

    assert state.state == "on"


async def test_random_binary_sensor_off(hass: __HAC_KEEP__) -> None:
    """Test the Random binary sensor."""
    config = {"binary_sensor": {"platform": "random", "name": "test"}}

    with patch(
        "universalassistant.components.random.binary_sensor.getrandbits",
        return_value=False,
    ):
        assert await async_setup_component(
            hass,
            "binary_sensor",
            config,
        )
        await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.test")

    assert state.state == "off"
