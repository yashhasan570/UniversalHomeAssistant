"""Test Schlage select."""

from collections.abc import Awaitable, Callable
from unittest.mock import Mock, patch

from pyschlage.lock import AUTO_LOCK_TIMES
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.schlage.const import DOMAIN
from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.translation import LOCALE_EN, async_get_translations

from . import MockSchlageConfigEntry


async def test_select_attributes(
    hass: __HAC_KEEP__,
    mock_add_config_entry: Callable[[], Awaitable[MockSchlageConfigEntry]],
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test select attributes."""
    with patch("universalassistant.components.schlage.PLATFORMS", [Platform.SELECT]):
        config_entry = await mock_add_config_entry()
        await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_select(
    hass: __HAC_KEEP__,
    mock_lock: Mock,
    mock_add_config_entry: Callable[[], Awaitable[MockSchlageConfigEntry]],
) -> None:
    """Test the auto-lock time select entity."""
    with patch("universalassistant.components.schlage.PLATFORMS", [Platform.SELECT]):
        await mock_add_config_entry()

    select = hass.states.get("select.vault_door_auto_lock_time")
    assert select is not None
    assert select.state == "15"

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: select.entity_id,
            SelectServiceArgument.OPTION: "30",
        },
        blocking=True,
    )
    mock_lock.set_auto_lock_time.assert_called_once_with(30)


async def test_auto_lock_time_translations(hass: __HAC_KEEP__) -> None:
    """Test all auto_lock_time select options are translated."""
    prefix = f"component.{DOMAIN}.entity.{Platform.SELECT.value}.auto_lock_time.state."
    translations = await async_get_translations(hass, LOCALE_EN, "entity", [DOMAIN])
    got_translation_states = {k for k in translations if k.startswith(prefix)}
    want_translation_states = {f"{prefix}{t}" for t in AUTO_LOCK_TIMES}
    assert want_translation_states == got_translation_states
