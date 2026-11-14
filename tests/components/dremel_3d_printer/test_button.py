"""Button tests for the Dremel 3D Printer integration."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.dremel_3d_printer.const import DOMAIN
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.setup import async_setup_component


@pytest.mark.parametrize(
    ("button", "function"),
    [
        ("cancel", "stop"),
        ("pause", "pause"),
        ("resume", "resume"),
    ],
)
@pytest.mark.usefixtures("connection", "entity_registry_enabled_by_default")
async def test_buttons(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    button: str,
    function: str,
) -> None:
    """Test button entities function."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    assert await async_setup_component(hass, DOMAIN, {})
    with patch(
        f"universalassistant.components.dremel_3d_printer.Dremel3DPrinter.{function}_print"
    ) as mock:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: [f"button.dremel_3d45_{button}_job"]},
            blocking=True,
        )
    assert mock.call_count == 1

    with (
        patch(
            f"universalassistant.components.dremel_3d_printer.Dremel3DPrinter.{function}_print",
            side_effect=RuntimeError,
        ) as mock,
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: [f"button.dremel_3d45_{button}_job"]},
            blocking=True,
        )
    assert mock.call_count == 1
