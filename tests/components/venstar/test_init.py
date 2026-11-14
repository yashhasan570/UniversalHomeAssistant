"""Tests of the initialization of the venstar integration."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.venstar.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_HOST, CONF_SSL
from universalassistant.core import __HAC_KEEP__

from . import VenstarColorTouchMock

TEST_HOST = "venstartest.localdomain"


async def test_setup_entry(hass: __HAC_KEEP__) -> None:
    """Validate that setup entry also configure the client."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: TEST_HOST,
            CONF_SSL: False,
        },
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.venstar.VenstarColorTouch._request",
            new=VenstarColorTouchMock._request,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_sensors",
            new=VenstarColorTouchMock.update_sensors,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_info",
            new=VenstarColorTouchMock.update_info,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_alerts",
            new=VenstarColorTouchMock.update_alerts,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.get_runtimes",
            new=VenstarColorTouchMock.get_runtimes,
        ),
        patch(
            "universalassistant.components.venstar.coordinator.VENSTAR_SLEEP",
            new=0,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)

    assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_entry_exception(hass: __HAC_KEEP__) -> None:
    """Validate that setup entry also configure the client."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: TEST_HOST,
            CONF_SSL: False,
        },
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.venstar.VenstarColorTouch._request",
            new=VenstarColorTouchMock._request,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_sensors",
            new=VenstarColorTouchMock.update_sensors,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_info",
            new=VenstarColorTouchMock.broken_update_info,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_alerts",
            new=VenstarColorTouchMock.update_alerts,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.get_runtimes",
            new=VenstarColorTouchMock.get_runtimes,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY


@pytest.mark.parametrize(
    ("failed_method", "target_method"),
    [
        ("failed_update_info", "update_info"),
        ("failed_update_sensors", "update_sensors"),
        ("failed_update_alerts", "update_alerts"),
        ("failed_get_runtimes", "get_runtimes"),
    ],
)
async def test_silent_failure_triggers_retry(
    hass: __HAC_KEEP__, failed_method: str, target_method: str
) -> None:
    """Validate coordinator handles library methods returning False."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: TEST_HOST,
            CONF_SSL: False,
        },
    )
    config_entry.add_to_hass(hass)

    # Map method names to their default (successful) mocks
    methods = {
        "update_info": VenstarColorTouchMock.update_info,
        "update_sensors": VenstarColorTouchMock.update_sensors,
        "update_alerts": VenstarColorTouchMock.update_alerts,
        "get_runtimes": VenstarColorTouchMock.get_runtimes,
    }
    # Override the target method with its failed variant
    methods[target_method] = getattr(VenstarColorTouchMock, failed_method)

    with (
        patch(
            "universalassistant.components.venstar.VenstarColorTouch._request",
            new=VenstarColorTouchMock._request,
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_info",
            new=methods["update_info"],
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_sensors",
            new=methods["update_sensors"],
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.update_alerts",
            new=methods["update_alerts"],
        ),
        patch(
            "universalassistant.components.venstar.VenstarColorTouch.get_runtimes",
            new=methods["get_runtimes"],
        ),
        patch(
            "universalassistant.components.venstar.coordinator.VENSTAR_SLEEP",
            new=0,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY
