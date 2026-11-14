"""Fixtures for tests."""

from http import HTTPStatus

import pytest
from pytest_universalassistant.common import load_fixture
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.const import CONTENT_TYPE_JSON


@pytest.fixture
def aioclient_mock_fixture(aioclient_mock: AiohttpClientMocker) -> None:
    """Fixture to provide a aioclient mocker."""
    aioclient_mock.get(
        "http://1.1.1.1:8080/status.json?show_avail=1",
        text=load_fixture("android_ip_webcam/status_data.json"),
        status=HTTPStatus.OK,
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )
    aioclient_mock.get(
        "http://1.1.1.1:8080/sensors.json",
        text=load_fixture("android_ip_webcam/sensor_data.json"),
        status=HTTPStatus.OK,
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )
