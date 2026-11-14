"""Test squeezebox update platform."""

import copy
from datetime import timedelta
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.squeezebox.const import (
    SENSOR_UPDATE_INTERVAL,
    STATUS_UPDATE_NEWPLUGINS,
)
from universalassistant.components.update import (
    ATTR_IN_PROGRESS,
    DOMAIN as UPDATE_DOMAIN,
    UpdateService,
)
from universalassistant.const import STATE_OFF, STATE_ON, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.util import dt as dt_util

from .conftest import FAKE_QUERY_RESPONSE


async def test_update_lms(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states and attributes."""

    # Setup component
    with (
        patch(
            "universalassistant.components.squeezebox.PLATFORMS",
            [Platform.UPDATE],
        ),
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)
    state = hass.states.get("update.fakelib_lyrion_music_server")

    assert state is not None
    assert state.state == STATE_ON


async def test_update_plugins_install_fallback(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states and attributes."""

    entity_id = "update.fakelib_updated_plugins"
    # Setup component
    with (
        patch(
            "universalassistant.components.squeezebox.PLATFORMS",
            [Platform.UPDATE],
        ),
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    polltime = 30
    with (
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=False,
        ),
        patch(
            "universalassistant.components.squeezebox.update.POLL_AFTER_INSTALL",
            polltime,
        ),
    ):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {
                CommonServiceArgument.ENTITY_ID: entity_id,
            },
            blocking=True,
        )

    state = hass.states.get(entity_id)
    attrs = state.attributes
    assert attrs[ATTR_IN_PROGRESS]

    with (
        patch(
            "universalassistant.components.squeezebox.Server.async_status",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        async_fire_time_changed(
            hass,
            dt_util.utcnow() + timedelta(seconds=polltime + 1),
        )
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    attrs = state.attributes
    assert not attrs[ATTR_IN_PROGRESS]


async def test_update_plugins_install_restart_fail(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states and attributes."""

    entity_id = "update.fakelib_updated_plugins"
    # Setup component
    with (
        patch(
            "universalassistant.components.squeezebox.PLATFORMS",
            [Platform.UPDATE],
        ),
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)

    with (
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=True,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {
                CommonServiceArgument.ENTITY_ID: entity_id,
            },
            blocking=True,
        )
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    attrs = state.attributes
    assert not attrs[ATTR_IN_PROGRESS]


async def test_update_plugins_install_ok(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states and attributes."""

    entity_id = "update.fakelib_updated_plugins"
    # Setup component
    with (
        patch(
            "universalassistant.components.squeezebox.PLATFORMS",
            [Platform.UPDATE],
        ),
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)

    with (
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=False,
        ),
    ):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {
                CommonServiceArgument.ENTITY_ID: entity_id,
            },
            blocking=True,
        )
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    attrs = state.attributes
    assert attrs[ATTR_IN_PROGRESS]

    resp = copy.deepcopy(FAKE_QUERY_RESPONSE)
    del resp[STATUS_UPDATE_NEWPLUGINS]

    with (
        patch(
            "universalassistant.components.squeezebox.Server.async_status",
            return_value=resp,
        ),
        patch(
            "universalassistant.components.squeezebox.Server.async_query",
            return_value=copy.deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        async_fire_time_changed(
            hass,
            dt_util.utcnow() + timedelta(seconds=SENSOR_UPDATE_INTERVAL + 1),
        )
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_OFF

    attrs = state.attributes
    assert not attrs[ATTR_IN_PROGRESS]
