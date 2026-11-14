"""Tests for the HDFury number platform."""

from datetime import timedelta
from unittest.mock import AsyncMock

from freezegun.api import FrozenDateTimeFactory
from hdfury import HDFuryError
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import STATE_UNAVAILABLE, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
import universalassistant.helpers.entity_registry as er

from . import setup_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test HDFury number entities."""

    await setup_integration(hass, mock_config_entry, [Platform.NUMBER])
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "method"),
    [
        ("number.hdfury_vrroom_02_oled_fade_timer", "set_oled_fade"),
        ("number.hdfury_vrroom_02_restart_timer", "set_reboot_timer"),
        ("number.hdfury_vrroom_02_unmute_delay", "set_audio_unmute"),
        ("number.hdfury_vrroom_02_earc_unmute_delay", "set_earc_unmute"),
    ],
)
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_set_value(
    hass: __HAC_KEEP__,
    mock_hdfury_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    method: str,
) -> None:
    """Test setting a device number value."""

    await setup_integration(hass, mock_config_entry, [Platform.NUMBER])

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {CommonServiceArgument.ENTITY_ID: entity_id, NumberServiceArgument.VALUE: 50},
        blocking=True,
    )

    getattr(mock_hdfury_client, method).assert_awaited_once_with("50")


@pytest.mark.parametrize(
    ("entity_id", "method"),
    [
        ("number.hdfury_vrroom_02_oled_fade_timer", "set_oled_fade"),
        ("number.hdfury_vrroom_02_restart_timer", "set_reboot_timer"),
        ("number.hdfury_vrroom_02_unmute_delay", "set_audio_unmute"),
        ("number.hdfury_vrroom_02_earc_unmute_delay", "set_earc_unmute"),
    ],
)
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_error(
    hass: __HAC_KEEP__,
    mock_hdfury_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    method: str,
) -> None:
    """Test set number value raises __HAC_KEEP__Error on API failure."""

    getattr(mock_hdfury_client, method).side_effect = HDFuryError()

    await setup_integration(hass, mock_config_entry, [Platform.NUMBER])

    with pytest.raises(
        __HAC_KEEP__Error,
        match="An error occurred while communicating with HDFury device",
    ):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: entity_id,
                NumberServiceArgument.VALUE: 50,
            },
            blocking=True,
        )


@pytest.mark.parametrize(
    ("entity_id"),
    [
        ("number.hdfury_vrroom_02_oled_fade_timer"),
        ("number.hdfury_vrroom_02_restart_timer"),
        ("number.hdfury_vrroom_02_unmute_delay"),
        ("number.hdfury_vrroom_02_earc_unmute_delay"),
    ],
)
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_entities_unavailable_on_error(
    hass: __HAC_KEEP__,
    mock_hdfury_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
    entity_id: str,
) -> None:
    """Test API error causes entities to become unavailable."""

    await setup_integration(hass, mock_config_entry, [Platform.NUMBER])

    mock_hdfury_client.get_info.side_effect = HDFuryError()

    freezer.tick(timedelta(seconds=61))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE
