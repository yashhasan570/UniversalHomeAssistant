"""Test the Reolink util functions."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from reolink_aio.exceptions import (
    ApiError,
    CredentialsInvalidError,
    InvalidContentTypeError,
    InvalidParameterError,
    LoginError,
    NoDataError,
    NotSupportedError,
    ReolinkConnectionError,
    ReolinkError,
    ReolinkTimeoutError,
    SubscriptionError,
    UnexpectedDataError,
)

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.components.reolink.const import DOMAIN
from universalassistant.components.reolink.util import get_device_uid_and_ch
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import device_registry as dr

from .conftest import TEST_CAM_NAME, TEST_UID, TEST_UID_CAM

DEV_ID_NVR = f"{TEST_UID}_{TEST_UID_CAM}"
DEV_ID_STANDALONE_CAM = f"{TEST_UID_CAM}"


@pytest.mark.parametrize(
    ("side_effect", "expected"),
    [
        (
            ApiError("Test error"),
            __HAC_KEEP__Error(translation_key="api_error"),
        ),
        (
            ApiError("Test error", translation_key="firmware_rate_limit"),
            __HAC_KEEP__Error(translation_key="firmware_rate_limit"),
        ),
        (
            ApiError("Test error", translation_key="not_in_strings.json"),
            __HAC_KEEP__Error(translation_key="api_error"),
        ),
        (
            CredentialsInvalidError("Test error"),
            __HAC_KEEP__Error(translation_key="invalid_credentials"),
        ),
        (
            InvalidContentTypeError("Test error"),
            __HAC_KEEP__Error(translation_key="invalid_content_type"),
        ),
        (
            InvalidParameterError("Test error"),
            ServiceValidationError(translation_key="invalid_parameter"),
        ),
        (
            LoginError("Test error"),
            __HAC_KEEP__Error(translation_key="login_error"),
        ),
        (
            NoDataError("Test error"),
            __HAC_KEEP__Error(translation_key="no_data"),
        ),
        (
            NotSupportedError("Test error"),
            __HAC_KEEP__Error(translation_key="not_supported"),
        ),
        (
            ReolinkConnectionError("Test error"),
            __HAC_KEEP__Error(translation_key="connection_error"),
        ),
        (
            ReolinkError("Test error"),
            __HAC_KEEP__Error(translation_key="unexpected"),
        ),
        (
            ReolinkTimeoutError("Test error"),
            __HAC_KEEP__Error(translation_key="timeout"),
        ),
        (
            SubscriptionError("Test error"),
            __HAC_KEEP__Error(translation_key="subscription_error"),
        ),
        (
            UnexpectedDataError("Test error"),
            __HAC_KEEP__Error(translation_key="unexpected_data"),
        ),
    ],
)
async def test_try_function(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    reolink_host: MagicMock,
    side_effect: ReolinkError,
    expected: __HAC_KEEP__Error,
) -> None:
    """Test try_function error translations using number entity."""
    reolink_host.volume.return_value = 80

    with patch("universalassistant.components.reolink.PLATFORMS", [Platform.NUMBER]):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.LOADED

    entity_id = f"{Platform.NUMBER}.{TEST_CAM_NAME}_volume"

    reolink_host.set_volume.side_effect = side_effect
    with pytest.raises(expected.__class__) as err:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: entity_id,
                NumberServiceArgument.VALUE: 50,
            },
            blocking=True,
        )

    assert err.value.translation_key == expected.translation_key


@pytest.mark.parametrize(
    ("identifiers"),
    [
        ({(DOMAIN, DEV_ID_NVR), (DOMAIN, DEV_ID_STANDALONE_CAM)}),
        ({(DOMAIN, DEV_ID_STANDALONE_CAM), (DOMAIN, DEV_ID_NVR)}),
    ],
)
async def test_get_device_uid_and_ch(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    reolink_host: MagicMock,
    device_registry: dr.DeviceRegistry,
    identifiers: set[tuple[str, str]],
) -> None:
    """Test get_device_uid_and_ch with multiple identifiers."""
    reolink_host.channels = [0]

    dev_entry = device_registry.async_get_or_create(
        identifiers=identifiers,
        config_entry_id=config_entry.entry_id,
        disabled_by=None,
    )

    # setup CH 0 and host entities/device
    with patch("universalassistant.components.reolink.PLATFORMS", [Platform.SWITCH]):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    result = get_device_uid_and_ch(
        dev_entry.identifiers, config_entry.runtime_data.host
    )
    # always get the uid and channel form the DEV_ID_NVR since is_nvr = True
    assert result == ([TEST_UID, TEST_UID_CAM], 0, False)
