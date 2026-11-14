"""Tests for the __HA_KEEP__ system state conditions."""

import probatio
import pytest

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import condition, system_state


async def _evaluate(hass: __HAC_KEEP__, condition_key: str) -> bool | None:
    """Validate and evaluate a system state condition."""
    config = await condition.async_validate_condition_config(
        hass, {"condition": condition_key}
    )
    checker = await condition.async_from_config(hass, config)
    return checker(hass)


async def test_restart_required(hass: __HAC_KEEP__) -> None:
    """Test the restart condition follows the restart flag."""
    assert await _evaluate(hass, "universalassistant.restart_required") is False

    system_state.async_set_universal_assistant_restart_required(hass, "hacs")

    assert await _evaluate(hass, "universalassistant.restart_required") is True


async def test_host_reboot_required(hass: __HAC_KEEP__) -> None:
    """Test the reboot condition follows the reboot flag."""
    assert await _evaluate(hass, "universalassistant.host_reboot_required") is False

    system_state.async_set_host_reboot_required(hass, True)

    assert await _evaluate(hass, "universalassistant.host_reboot_required") is True


async def test_rejects_options(hass: __HAC_KEEP__) -> None:
    """Test the conditions do not take options."""
    with pytest.raises(probatio.Invalid):
        await condition.async_validate_condition_config(
            hass,
            {"condition": "universalassistant.restart_required", "options": {"x": 1}},
        )
