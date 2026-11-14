"""Test the Universal Universal Home Assistant Green integration."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, MockModule, mock_integration

from universalassistant.components.hassio import DOMAIN as HASSIO_DOMAIN, HassioNotReadyError
from universalassistant.components.universalassistant_green.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_setup_entry(hass: UniversalAssistant) -> None:
    """Test setup of a config entry."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        return_value={"board": "green"},
    ) as mock_get_os_info:
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert len(mock_get_os_info.mock_calls) == 1

    # Test unloading the config entry
    assert await hass.config_entries.async_unload(config_entry.entry_id)


async def test_setup_entry_no_hassio(hass: UniversalAssistant) -> None:
    """Test setup of a config entry without hassio."""
    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    assert len(hass.config_entries.async_entries()) == 1

    with patch(
        "universalassistant.components.universalassistant_green.get_os_info"
    ) as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 0
    assert len(hass.config_entries.async_entries()) == 0


async def test_setup_entry_wrong_board(hass: UniversalAssistant) -> None:
    """Test setup of a config entry with wrong board type."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    assert len(hass.config_entries.async_entries()) == 1

    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        return_value={"board": "generic-x86-64"},
    ) as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 1
    assert len(hass.config_entries.async_entries()) == 0


@pytest.mark.parametrize(
    ("hassio", "board", "reason"),
    [
        pytest.param(
            False,
            None,
            "Universal Universal Home Assistant is not running on Universal Universal Home Assistant OS, the Universal Universal Home Assistant"
            " Green entry will be removed",
            id="no_hassio",
        ),
        pytest.param(
            True,
            "generic-x86-64",
            "Universal Universal Home Assistant is not running on a Universal Universal Home Assistant Green"
            " (generic-x86-64), the Universal Universal Home Assistant Green entry will be removed",
            id="wrong_board",
        ),
    ],
)
async def test_setup_entry_error_reason(
    hass: UniversalAssistant, hassio: bool, board: str | None, reason: str
) -> None:
    """Test the setup error reason when the entry is about to be removed."""
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.universalassistant_green.is_hassio",
            return_value=hassio,
        ),
        patch(
            "universalassistant.components.universalassistant_green.get_os_info",
            return_value={"board": board},
        ),
        patch.object(hass.config_entries, "async_remove", AsyncMock()) as mock_remove,
    ):
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_ERROR
    assert config_entry.reason == reason
    mock_remove.assert_awaited_once_with(config_entry.entry_id)


async def test_setup_entry_wait_hassio(hass: UniversalAssistant) -> None:
    """Test setup of a config entry when hassio has not fetched os_info."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        side_effect=HassioNotReadyError,
    ) as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 1
    assert config_entry.state is ConfigEntryState.SETUP_RETRY
