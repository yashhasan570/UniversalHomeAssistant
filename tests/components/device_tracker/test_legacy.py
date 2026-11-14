"""Tests for the legacy device tracker component."""

from unittest.mock import mock_open, patch

import pytest
from pytest_universalassistant.common import assert_setup_component, patch_yaml_files
from pytest_universalassistant.components.repairs import (
    process_repair_fix_flow,
    start_repair_fix_flow,
)
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components import device_tracker
from universalassistant.components.device_tracker import legacy
from universalassistant.const import CONF_PLATFORM
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers import issue_registry as ir
from universalassistant.setup import async_setup_component
from universalassistant.util.yaml import dump

from .common import MockScanner, mock_legacy_device_tracker_setup

TEST_PLATFORM = {device_tracker.DOMAIN: {CONF_PLATFORM: "test"}}


def test_remove_device_from_config(hass: __HAC_KEEP__) -> None:
    """Test the removal of a device from a config."""
    yaml_devices = {
        "test": {
            "hide_if_away": True,
            "mac": "00:11:22:33:44:55",
            "name": "Test name",
            "picture": "/local/test.png",
            "track": True,
        },
        "test2": {
            "hide_if_away": True,
            "mac": "00:ab:cd:33:44:55",
            "name": "Test2",
            "picture": "/local/test2.png",
            "track": True,
        },
    }
    mopen = mock_open()

    files = {legacy.YAML_DEVICES: dump(yaml_devices)}
    with (
        patch_yaml_files(files, True),
        patch("universalassistant.components.device_tracker.legacy.open", mopen),
    ):
        legacy.remove_device_from_config(hass, "test")

    mopen().write.assert_called_once_with(
        "test2:\n"
        "  hide_if_away: true\n"
        "  mac: 00:ab:cd:33:44:55\n"
        "  name: Test2\n"
        "  picture: /local/test2.png\n"
        "  track: true\n"
    )


async def test_see_service_deprecation_warning(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test deprecation warning when calling device_tracker.see."""
    mock_legacy_device_tracker_setup(hass, MockScanner())
    with assert_setup_component(1, device_tracker.DOMAIN):
        assert await async_setup_component(hass, device_tracker.DOMAIN, TEST_PLATFORM)
        await hass.async_block_till_done()

    await hass.services.async_call(
        device_tracker.DOMAIN,
        legacy.SERVICE_SEE,
        {"dev_id": "test_device", "location_name": "Work"},
        blocking=True,
    )

    assert (
        "The device_tracker.see action is deprecated and will be removed in "
        "__HA_KEEP__ Core 2027.5"
    ) in caplog.text

    issue = issue_registry.async_get_issue(
        device_tracker.DOMAIN, "deprecated_see_action"
    )
    assert issue is not None
    assert issue.is_fixable is True
    assert issue.is_persistent is True
    assert issue.breaks_in_ha_version == "2027.5.0"

    caplog.clear()

    # Second call should not produce another warning
    await hass.services.async_call(
        device_tracker.DOMAIN,
        legacy.SERVICE_SEE,
        {"dev_id": "test_device", "location_name": "Work"},
        blocking=True,
    )

    assert "deprecated" not in caplog.text


async def test_see_service_repair_flow(
    hass: __HAC_KEEP__,
    issue_registry: ir.IssueRegistry,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test confirming the repair issue removes it from the issue registry."""
    mock_legacy_device_tracker_setup(hass, MockScanner())
    with assert_setup_component(1, device_tracker.DOMAIN):
        assert await async_setup_component(hass, device_tracker.DOMAIN, TEST_PLATFORM)
        await hass.async_block_till_done()

    await hass.services.async_call(
        device_tracker.DOMAIN,
        legacy.SERVICE_SEE,
        {"dev_id": "test_device", "location_name": "Work"},
        blocking=True,
    )

    assert issue_registry.async_get_issue(
        device_tracker.DOMAIN, "deprecated_see_action"
    )

    assert await async_setup_component(hass, "repairs", {})
    client = await hass_client()

    result = await start_repair_fix_flow(
        client, device_tracker.DOMAIN, "deprecated_see_action"
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "confirm"

    result = await process_repair_fix_flow(client, result["flow_id"], {})

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert (
        issue_registry.async_get_issue(device_tracker.DOMAIN, "deprecated_see_action")
        is None
    )

    # Calling the action again after confirming recreates the issue.
    await hass.services.async_call(
        device_tracker.DOMAIN,
        legacy.SERVICE_SEE,
        {"dev_id": "test_device", "location_name": "Work"},
        blocking=True,
    )

    assert issue_registry.async_get_issue(
        device_tracker.DOMAIN, "deprecated_see_action"
    )


async def test_legacy_platform_setup_deprecation_warning(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test deprecation warning when setting up a legacy device tracker platform."""
    mock_legacy_device_tracker_setup(hass, MockScanner())
    with assert_setup_component(1, device_tracker.DOMAIN):
        assert await async_setup_component(hass, device_tracker.DOMAIN, TEST_PLATFORM)
        await hass.async_block_till_done()

    assert (
        "The legacy device tracker platform test.device_tracker is being set up; "
        "legacy device trackers are deprecated and will be removed in Home "
        "Assistant Core 2027.5, please migrate to an integration which "
        "uses a modern config entry based device tracker"
    ) in caplog.text
