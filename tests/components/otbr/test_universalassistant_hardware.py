"""Test Universal Home Assistant Hardware platform for OTBR."""

from unittest.mock import AsyncMock, Mock, call, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.universalassistant_hardware import (
    DOMAIN as HOMEASSISTANT_HARDWARE_DOMAIN,
)
from universalassistant.components.universalassistant_hardware.helpers import (
    async_register_firmware_info_callback,
)
from universalassistant.components.universalassistant_hardware.util import (
    ApplicationType,
    FirmwareInfo,
    OwningAddon,
    OwningIntegration,
)
from universalassistant.components.otbr import DOMAIN
from universalassistant.components.otbr.universalassistant_hardware import async_get_firmware_info
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.setup import async_setup_component

from . import TEST_COPROCESSOR_VERSION

DEVICE_PATH = (
    "/dev/serial/by-id/usb-Nabu_Casa_Home_Assistant_Connect_ZBT-1"
    "_9ab1da1ea4b3ed11956f4eaca7669f5d-if00-port0"
)


async def test_get_firmware_info(hass: UniversalAssistant) -> None:
    """Test `async_get_firmware_info`."""

    otbr = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={
            "url": "http://core_openthread_border_router:8888",
        },
        version=1,
    )
    otbr.add_to_hass(hass)
    otbr.mock_state(hass, ConfigEntryState.LOADED)

    otbr.runtime_data = AsyncMock()
    otbr.runtime_data.get_coprocessor_version.return_value = TEST_COPROCESSOR_VERSION

    with (
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.is_hassio",
            return_value=True,
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.AddonManager",
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.get_otbr_addon_firmware_info",
            return_value=FirmwareInfo(
                device=DEVICE_PATH,
                firmware_type=ApplicationType.SPINEL,
                firmware_version=None,
                source="otbr",
                owners=[
                    OwningAddon(slug="core_openthread_border_router"),
                ],
            ),
        ),
    ):
        fw_info = await async_get_firmware_info(hass, otbr)

    assert fw_info == FirmwareInfo(
        device=DEVICE_PATH,
        firmware_type=ApplicationType.SPINEL,
        firmware_version=TEST_COPROCESSOR_VERSION,
        source="otbr",
        owners=[
            OwningIntegration(config_entry_id=otbr.entry_id),
            OwningAddon(slug="core_openthread_border_router"),
        ],
    )


async def test_get_firmware_info_ignored(hass: UniversalAssistant) -> None:
    """Test `async_get_firmware_info` with ignored entry."""

    otbr = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={},
        version=1,
    )
    otbr.add_to_hass(hass)

    fw_info = await async_get_firmware_info(hass, otbr)
    assert fw_info is None


async def test_get_firmware_info_no_coprocessor_version(hass: UniversalAssistant) -> None:
    """Test `async_get_firmware_info` with no coprocessor version support."""

    otbr = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={
            "url": "http://core_openthread_border_router:8888",
        },
        version=1,
    )
    otbr.add_to_hass(hass)
    otbr.mock_state(hass, ConfigEntryState.LOADED)

    otbr.runtime_data = AsyncMock()
    otbr.runtime_data.get_coprocessor_version.side_effect = UniversalAssistantError()

    with (
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.is_hassio",
            return_value=True,
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.AddonManager",
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.get_otbr_addon_firmware_info",
            return_value=FirmwareInfo(
                device=DEVICE_PATH,
                firmware_type=ApplicationType.SPINEL,
                firmware_version=None,
                source="otbr",
                owners=[
                    OwningAddon(slug="core_openthread_border_router"),
                ],
            ),
        ),
    ):
        fw_info = await async_get_firmware_info(hass, otbr)

    assert fw_info == FirmwareInfo(
        device=DEVICE_PATH,
        firmware_type=ApplicationType.SPINEL,
        firmware_version=None,
        source="otbr",
        owners=[
            OwningIntegration(config_entry_id=otbr.entry_id),
            OwningAddon(slug="core_openthread_border_router"),
        ],
    )


@pytest.mark.parametrize(
    ("version", "expected_version"),
    [
        ((TEST_COPROCESSOR_VERSION,), TEST_COPROCESSOR_VERSION),
        (UniversalAssistantError(), None),
    ],
)
async def test_hardware_firmware_info_provider_notification(
    hass: UniversalAssistant,
    version: str | Exception,
    expected_version: str | None,
    get_active_dataset_tlvs: AsyncMock,
    get_border_agent_id: AsyncMock,
    get_extended_address: AsyncMock,
    get_coprocessor_version: AsyncMock,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test that the OTBR provides hardware and firmware information."""
    otbr = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={
            "url": "http://core_openthread_border_router:8888",
        },
        version=1,
    )
    otbr.add_to_hass(hass)

    await async_setup_component(hass, HOMEASSISTANT_HARDWARE_DOMAIN, {})

    callback = Mock()
    async_register_firmware_info_callback(hass, DEVICE_PATH, callback)

    with (
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.is_hassio",
            return_value=True,
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.AddonManager",
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.get_otbr_addon_firmware_info",
            return_value=FirmwareInfo(
                device=DEVICE_PATH,
                firmware_type=ApplicationType.SPINEL,
                firmware_version=None,
                source="otbr",
                owners=[
                    OwningAddon(slug="core_openthread_border_router"),
                ],
            ),
        ),
    ):
        get_coprocessor_version.side_effect = version
        await hass.config_entries.async_setup(otbr.entry_id)

    assert callback.mock_calls == [
        call(
            FirmwareInfo(
                device=DEVICE_PATH,
                firmware_type=ApplicationType.SPINEL,
                firmware_version=expected_version,
                source="otbr",
                owners=[
                    OwningIntegration(config_entry_id=otbr.entry_id),
                    OwningAddon(slug="core_openthread_border_router"),
                ],
            )
        )
    ]


async def test_get_firmware_info_remote_otbr(hass: UniversalAssistant) -> None:
    """Test `async_get_firmware_info` with no coprocessor version support."""

    otbr = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={
            "url": "http://192.168.1.10:8888",
        },
        version=1,
    )
    otbr.add_to_hass(hass)
    otbr.mock_state(hass, ConfigEntryState.LOADED)

    otbr.runtime_data = AsyncMock()
    otbr.runtime_data.get_coprocessor_version.return_value = TEST_COPROCESSOR_VERSION

    with (
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.is_hassio",
            return_value=True,
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.AddonManager",
        ),
        patch(
            "universalassistant.components.otbr.universalassistant_hardware.get_otbr_addon_firmware_info",
            return_value=None,
        ),
    ):
        fw_info = await async_get_firmware_info(hass, otbr)

    assert fw_info is None
