"""Test the Prowl notifications."""

from typing import Any
from unittest.mock import AsyncMock

from freezegun.api import FrozenDateTimeFactory
import probatio
import prowlpy
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import notify
from universalassistant.components.prowl.const import DOMAIN
from universalassistant.components.prowl.services import ProwlService, ProwlServiceArgument
from universalassistant.config_entries import SOURCE_IMPORT
from universalassistant.const import CONF_API_KEY, STATE_UNKNOWN
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import issue_registry as ir

from .conftest import ENTITY_ID, TEST_API_KEY

SERVICE_DATA = {"message": "Test Notification", "title": "Test Title"}

EXPECTED_SEND_PARAMETERS = {
    "application": "Universal-Assistant",
    "event": "Test Title",
    "description": "Test Notification",
    "priority": 0,
    "url": None,
}


@pytest.mark.usefixtures("configure_prowl_through_yaml")
async def test_send_notification_service(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
) -> None:
    """Set up Prowl, call notify service, and check API call."""
    assert hass.services.has_service(notify.DOMAIN, DOMAIN)
    await hass.services.async_call(
        notify.DOMAIN,
        DOMAIN,
        SERVICE_DATA,
        blocking=True,
    )

    mock_prowlpy.post.assert_called_once_with(**EXPECTED_SEND_PARAMETERS)


async def test_send_notification_entity_service(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    mock_prowlpy_config_entry: MockConfigEntry,
) -> None:
    """Set up Prowl via config entry, call notify service, and check API call."""
    mock_prowlpy_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_prowlpy_config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.services.has_service(notify.DOMAIN, notify.SERVICE_SEND_MESSAGE)
    await hass.services.async_call(
        notify.DOMAIN,
        notify.SERVICE_SEND_MESSAGE,
        {
            "entity_id": ENTITY_ID,
            notify.ATTR_MESSAGE: SERVICE_DATA["message"],
            notify.ATTR_TITLE: SERVICE_DATA["title"],
        },
        blocking=True,
    )

    mock_prowlpy.post.assert_called_once_with(**EXPECTED_SEND_PARAMETERS)


@pytest.mark.parametrize(
    ("prowlpy_side_effect", "raised_exception", "exception_message"),
    [
        (
            prowlpy.APIError("Internal server error"),
            __HAC_KEEP__Error,
            "Unexpected error when calling the Prowl API: Internal server error",
        ),
        (
            TimeoutError,
            __HAC_KEEP__Error,
            "Timeout accessing the Prowl API",
        ),
        (
            prowlpy.APIError(f"Invalid API key: {TEST_API_KEY}"),
            __HAC_KEEP__Error,
            "Invalid API key for the Prowl service",
        ),
        (
            prowlpy.APIError(
                "Not accepted: Your IP address has exceeded the API limit"
            ),
            __HAC_KEEP__Error,
            "The Prowl service reported that the rate limit was exceeded",
        ),
        (
            SyntaxError(),
            SyntaxError,
            None,
        ),
    ],
)
async def test_fail_send_notification_entity_service(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    mock_prowlpy_config_entry: MockConfigEntry,
    prowlpy_side_effect: Exception,
    raised_exception: type[Exception],
    exception_message: str | None,
) -> None:
    """Set up Prowl via config entry, call notify service, and check API call."""
    mock_prowlpy_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_prowlpy_config_entry.entry_id)
    await hass.async_block_till_done()

    mock_prowlpy.post.side_effect = prowlpy_side_effect

    assert hass.services.has_service(notify.DOMAIN, notify.SERVICE_SEND_MESSAGE)
    with pytest.raises(raised_exception, match=exception_message):
        await hass.services.async_call(
            notify.DOMAIN,
            notify.SERVICE_SEND_MESSAGE,
            {
                "entity_id": ENTITY_ID,
                notify.ATTR_MESSAGE: SERVICE_DATA["message"],
                notify.ATTR_TITLE: SERVICE_DATA["title"],
            },
            blocking=True,
        )

    mock_prowlpy.post.assert_called_once_with(**EXPECTED_SEND_PARAMETERS)


@pytest.mark.parametrize(
    ("prowlpy_side_effect", "raised_exception", "exception_message"),
    [
        (
            prowlpy.APIError("Internal server error"),
            __HAC_KEEP__Error,
            "Unexpected error when calling the Prowl API: Internal server error",
        ),
        (
            TimeoutError,
            __HAC_KEEP__Error,
            "Timeout accessing the Prowl API",
        ),
        (
            prowlpy.APIError(f"Invalid API key: {TEST_API_KEY}"),
            __HAC_KEEP__Error,
            "Invalid API key for the Prowl service",
        ),
        (
            prowlpy.APIError(
                "Not accepted: Your IP address has exceeded the API limit"
            ),
            __HAC_KEEP__Error,
            "The Prowl service reported that the rate limit was exceeded",
        ),
        (
            SyntaxError(),
            SyntaxError,
            None,
        ),
    ],
)
@pytest.mark.usefixtures("configure_prowl_through_yaml")
async def test_fail_send_notification(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    prowlpy_side_effect: Exception,
    raised_exception: type[Exception],
    exception_message: str | None,
) -> None:
    """Sending a message via Prowl with a failure."""
    mock_prowlpy.post.side_effect = prowlpy_side_effect

    assert hass.services.has_service(notify.DOMAIN, DOMAIN)
    with pytest.raises(raised_exception, match=exception_message):
        await hass.services.async_call(
            notify.DOMAIN,
            DOMAIN,
            SERVICE_DATA,
            blocking=True,
        )

    mock_prowlpy.post.assert_called_once_with(**EXPECTED_SEND_PARAMETERS)


@pytest.mark.parametrize(
    ("service_data", "expected_send_parameters"),
    [
        (
            {"message": "Test Notification", "title": "Test Title"},
            {
                "application": "Universal-Assistant",
                "event": "Test Title",
                "description": "Test Notification",
                "priority": 0,
                "url": None,
            },
        )
    ],
)
@pytest.mark.usefixtures("configure_prowl_through_yaml")
async def test_other_exception_send_notification(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    service_data: dict[str, Any],
    expected_send_parameters: dict[str, Any],
) -> None:
    """Sending a message via Prowl with a general unhandled exception."""
    mock_prowlpy.post.side_effect = SyntaxError

    assert hass.services.has_service(notify.DOMAIN, DOMAIN)
    with pytest.raises(SyntaxError):
        await hass.services.async_call(
            notify.DOMAIN,
            DOMAIN,
            SERVICE_DATA,
            blocking=True,
        )

    mock_prowlpy.post.assert_called_once_with(**expected_send_parameters)


@pytest.mark.parametrize(
    ("service_data", "expected_send_parameters"),
    [
        pytest.param(
            {notify.ATTR_MESSAGE: "Test Notification"},
            {
                "application": "Universal-Assistant",
                "event": notify.ATTR_TITLE_DEFAULT,
                "description": "Test Notification",
                "priority": 0,
                "url": None,
            },
            id="message_only",
        ),
        pytest.param(
            {
                notify.ATTR_MESSAGE: "Test Notification",
                notify.ATTR_TITLE: "Test Title",
                "priority": "emergency",
                "url": "https://www.universalassistant.io",
            },
            {
                "application": "Universal-Assistant",
                "event": "Test Title",
                "description": "Test Notification",
                "priority": 2,
                "url": "https://www.universalassistant.io",
            },
            id="all_options",
        ),
        pytest.param(
            {notify.ATTR_MESSAGE: "Test Notification", "priority": "very_low"},
            {
                "application": "Universal-Assistant",
                "event": notify.ATTR_TITLE_DEFAULT,
                "description": "Test Notification",
                "priority": -2,
                "url": None,
            },
            id="very_low_priority",
        ),
        pytest.param(
            {
                notify.ATTR_MESSAGE: "Test Notification",
                "url": "shortcuts://run-shortcut?name=Lights",
            },
            {
                "application": "Universal-Assistant",
                "event": notify.ATTR_TITLE_DEFAULT,
                "description": "Test Notification",
                "priority": 0,
                "url": "shortcuts://run-shortcut?name=Lights",
            },
            id="app_url_scheme",
        ),
    ],
)
@pytest.mark.usefixtures("prowl_notification_entity")
async def test_prowl_send_message_action(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    freezer: FrozenDateTimeFactory,
    service_data: dict[str, Any],
    expected_send_parameters: dict[str, Any],
) -> None:
    """Test the prowl.send_message entity action."""
    freezer.move_to("2026-10-03T12:00:00+00:00")
    assert (state := hass.states.get(ENTITY_ID))
    assert state.state == STATE_UNKNOWN

    await hass.services.async_call(
        DOMAIN,
        ProwlService.SEND_MESSAGE,
        {"entity_id": ENTITY_ID, **service_data},
        blocking=True,
    )

    mock_prowlpy.post.assert_called_once_with(**expected_send_parameters)
    assert (state := hass.states.get(ENTITY_ID))
    assert state.state == "2026-10-03T12:00:00+00:00"


@pytest.mark.parametrize(
    "service_data",
    [
        pytest.param({"priority": "invalid"}, id="invalid_priority"),
        pytest.param({"url": f"https://{'a' * 512}.com"}, id="url_too_long"),
    ],
)
@pytest.mark.usefixtures("prowl_notification_entity")
async def test_prowl_send_message_action_invalid(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
    service_data: dict[str, Any],
) -> None:
    """Test the prowl.send_message entity action rejects invalid input."""
    with pytest.raises(probatio.Invalid):
        await hass.services.async_call(
            DOMAIN,
            ProwlService.SEND_MESSAGE,
            {
                "entity_id": ENTITY_ID,
                ProwlServiceArgument.MESSAGE: "Test Notification",
                **service_data,
            },
            blocking=True,
        )

    mock_prowlpy.post.assert_not_called()


@pytest.mark.usefixtures("prowl_notification_entity")
async def test_prowl_send_message_action_error(
    hass: __HAC_KEEP__,
    mock_prowlpy: AsyncMock,
) -> None:
    """Test the prowl.send_message entity action raises on API errors."""
    mock_prowlpy.post.side_effect = TimeoutError

    with pytest.raises(__HAC_KEEP__Error, match="Timeout accessing the Prowl API"):
        await hass.services.async_call(
            DOMAIN,
            ProwlService.SEND_MESSAGE,
            {"entity_id": ENTITY_ID, ProwlServiceArgument.MESSAGE: "Test Notification"},
            blocking=True,
        )

    assert (state := hass.states.get(ENTITY_ID))
    assert state.state == STATE_UNKNOWN


@pytest.mark.usefixtures("configure_prowl_through_yaml", "mock_prowlpy")
async def test_deprecated_legacy_notify_action(
    hass: __HAC_KEEP__,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test the legacy notify action creates a deprecation issue."""
    assert not issue_registry.async_get_issue(
        DOMAIN, f"deprecated_notify_action_{DOMAIN}"
    )

    await hass.services.async_call(
        notify.DOMAIN,
        DOMAIN,
        SERVICE_DATA,
        blocking=True,
    )

    issue = issue_registry.async_get_issue(DOMAIN, f"deprecated_notify_action_{DOMAIN}")
    assert issue
    assert issue.breaks_in_ha_version == "2027.5.0"
    assert issue.translation_placeholders["action"] == f"notify.{DOMAIN}"


@pytest.mark.usefixtures("mock_prowlpy")
async def test_deprecated_legacy_notify_action_from_imported_entry(
    hass: __HAC_KEEP__,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test the legacy action set up from an imported entry creates the issue."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="phone",
        data={CONF_API_KEY: TEST_API_KEY},
        source=SOURCE_IMPORT,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    # The legacy action is set up in a background task of the entry
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.services.has_service(notify.DOMAIN, "phone")

    await hass.services.async_call(notify.DOMAIN, "phone", SERVICE_DATA, blocking=True)

    issue = issue_registry.async_get_issue(DOMAIN, "deprecated_notify_action_phone")
    assert issue
    assert issue.translation_placeholders["action"] == "notify.phone"
