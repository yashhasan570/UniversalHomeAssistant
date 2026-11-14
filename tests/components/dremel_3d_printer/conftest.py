"""Configure tests for the Dremel 3D Printer integration."""

from http import HTTPStatus
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, load_fixture
import requests_mock

from universalassistant.components.dremel_3d_printer.const import DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__

HOST = "1.2.3.4"
CONF_DATA = {CONF_HOST: HOST}


def create_entry(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Create fixture for adding config entry in __HA_KEEP__."""
    entry = MockConfigEntry(domain=DOMAIN, data=CONF_DATA, unique_id="123456789")
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def config_entry(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Add config entry in __HA_KEEP__."""
    return create_entry(hass)


@pytest.fixture
def connection() -> None:
    """Mock Dremel 3D Printer connection."""
    with requests_mock.Mocker() as mock:
        mock.post(
            f"http://{HOST}/command",
            response_list=[
                {"text": load_fixture("dremel_3d_printer/command_1.json")},
                {"text": load_fixture("dremel_3d_printer/command_2.json")},
                {"text": load_fixture("dremel_3d_printer/command_1.json")},
                {"text": load_fixture("dremel_3d_printer/command_2.json")},
            ],
        )

        mock.post(
            f"https://{HOST}:11134/getHomeMessage",
            text=load_fixture("dremel_3d_printer/get_home_message.json"),
            status_code=HTTPStatus.OK,
        )
        yield


def patch_async_setup_entry():
    """Patch the async entry setup of Dremel 3D Printer."""
    return patch(
        "universalassistant.components.dremel_3d_printer.async_setup_entry",
        return_value=None,
    )
