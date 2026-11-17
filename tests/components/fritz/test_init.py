"""Tests for Fritz!Tools."""

import re
from unittest.mock import patch
from xml.etree.ElementTree import ParseError

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import core
from universalassistant.components.device_tracker import (
    CONF_CONSIDER_HOME,
    DEFAULT_CONSIDER_HOME,
)
from universalassistant.components.fritz.const import (
    DOMAIN,
    FRITZ_AUTH_EXCEPTIONS,
    FRITZ_EXCEPTIONS,
)
from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import TargetKey
from universalassistant.core import UniversalAssistant

from .const import MOCK_USER_DATA


async def test_setup(
    hass: UniversalAssistant,
    fc_class_mock,
    fh_class_mock,
    fs_class_mock,
) -> None:
    """Test setup and unload of Fritz!Tools."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_options_reload(
    hass: UniversalAssistant,
    fc_class_mock,
    fh_class_mock,
    fs_class_mock,
) -> None:
    """Test reload of Fritz!Tools, when options changed."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_USER_DATA,
        options={CONF_CONSIDER_HOME: DEFAULT_CONSIDER_HOME.total_seconds()},
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.config_entries.ConfigEntries.async_reload",
        return_value=None,
    ) as mock_reload:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state is ConfigEntryState.LOADED

        result = await hass.config_entries.options.async_init(entry.entry_id)
        await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={CONF_CONSIDER_HOME: 60},
        )
        await hass.async_block_till_done()
        mock_reload.assert_called_once()


@pytest.mark.parametrize(
    "error",
    FRITZ_AUTH_EXCEPTIONS,
)
async def test_setup_auth_fail(hass: UniversalAssistant, error) -> None:
    """Test starting a flow by user with an already configured device."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.fritz.coordinator.FritzConnectionCached",
        side_effect=error,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.parametrize(
    "error",
    FRITZ_EXCEPTIONS,
)
async def test_setup_fail(hass: UniversalAssistant, error) -> None:
    """Test starting a flow by user with an already configured device."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.fritz.coordinator.FritzConnectionCached",
        side_effect=error,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.state.recoverable is True
    assert entry.error_reason_translation_key == "error_connecting"


async def test_setup_fail_parse_error(hass: UniversalAssistant, fc_class_mock) -> None:
    """Test setup failure due to parse error while fetching device data."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.fritz.coordinator.FritzStatus.get_device_info"
        ) as fs_mock,
    ):
        fs_mock.side_effect = ParseError("boom")
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.error_reason_translation_key == "error_parse_device_info"


@pytest.mark.parametrize(
    "upnp_config",
    [
        pytest.param({"NewEnable": False}, id="disabled"),
        pytest.param({}, id="missing_key"),
    ],
)
async def test_upnp_missing(
    hass: UniversalAssistant,
    fc_class_mock,
    fh_class_mock,
    fs_class_mock,
    upnp_config: dict[str, bool],
) -> None:
    """Test UPNP configuration is missing."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.fritz.coordinator.AvmWrapper.async_get_upnp_configuration",
            return_value=upnp_config,
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.state.recoverable is True
    assert entry.error_reason_translation_key == "error_upnp_disabled"


async def test_execute_action_while_shutdown(
    hass: UniversalAssistant,
    caplog: pytest.LogCaptureFixture,
    fc_class_mock,
    fh_class_mock,
    fs_class_mock,
) -> None:
    """Test Fritz!Tools actions executed during shutdown of UniversalAssistant."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    hass.set_state(core.CoreState.stopping)
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: "switch.mock_title_wi_fi_guest"},
        blocking=True,
    )

    assert re.search(
        r"Cannot execute (.+): UniversalAssistant is shutting down", caplog.text
    )
