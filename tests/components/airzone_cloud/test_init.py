"""Define tests for the Airzone Cloud init."""

from unittest.mock import patch

from aioairzone_cloud.exceptions import AirzoneTimeout
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.airzone_cloud.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from .util import CONFIG, WS_ID, WS_ID_AIDOO, async_init_integration


async def test_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test unload."""

    config_entry = MockConfigEntry(
        data=CONFIG,
        domain=DOMAIN,
        unique_id="airzone_cloud_unique_id",
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.login",
            return_value=None,
        ),
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.logout",
            return_value=None,
        ),
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.list_installations",
            return_value=[],
        ),
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.update_installation",
            return_value=None,
        ),
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.update",
            return_value=None,
        ),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_device_via_device(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test that child devices are linked to their via_device parents."""
    await async_init_integration(hass)

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]

    ws_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, WS_ID), config_entry.entry_id
    )
    assert ws_device is not None
    assert ws_device.via_device_id is None

    ws_aidoo_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, WS_ID_AIDOO), config_entry.entry_id
    )
    assert ws_aidoo_device is not None

    system_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "system1"), config_entry.entry_id
    )
    assert system_device is not None
    assert system_device.via_device_id == ws_device.id

    zone_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "zone1"), config_entry.entry_id
    )
    assert zone_device is not None
    assert zone_device.via_device_id == system_device.id

    dhw_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "dhw1"), config_entry.entry_id
    )
    assert dhw_device is not None
    assert dhw_device.via_device_id == ws_device.id

    aidoo_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "aidoo1"), config_entry.entry_id
    )
    assert aidoo_device is not None
    assert aidoo_device.via_device_id == ws_aidoo_device.id


async def test_init_api_timeout(hass: __HAC_KEEP__) -> None:
    """Test API timeouts when loading the Airzone Cloud integration."""

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.login",
        side_effect=AirzoneTimeout,
    ):
        config_entry = MockConfigEntry(
            data=CONFIG,
            domain=DOMAIN,
            unique_id="airzone_cloud_unique_id",
        )
        config_entry.add_to_hass(hass)

        assert await hass.config_entries.async_setup(config_entry.entry_id) is False
