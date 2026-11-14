"""The tests for the Universal Universal Home Assistant SpaceAPI component."""

from http import HTTPStatus

from aiohttp.test_utils import TestClient
import pytest
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.spaceapi import (
    ATTR_SENSOR_LOCATION,
    DOMAIN,
    SPACEAPI_VERSION,
    URL_API_SPACEAPI,
)
from universalassistant.const import ATTR_UNIT_OF_MEASUREMENT, PERCENTAGE, UnitOfTemperature
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

CONFIG = {
    DOMAIN: {
        "space": "Home",
        "logo": "https://universalassistant.io/logo.png",
        "url": "https://universalassistant.io",
        "location": {"address": "In your Home"},
        "contact": {"email": "hello@universalassistant.io"},
        "issue_report_channels": ["email"],
        "state": {
            "entity_id": "test.test_door",
            "icon_open": "https://universalassistant.io/open.png",
            "icon_closed": "https://universalassistant.io/close.png",
        },
        "sensors": {
            "temperature": ["test.temp1", "test.temp2", "test.temp3"],
            "humidity": ["test.hum1"],
        },
        "spacefed": {"spacenet": True, "spacesaml": False, "spacephone": True},
        "cam": ["https://universalassistant.io/cam1", "https://universalassistant.io/cam2"],
        "stream": {
            "m4": "https://universalassistant.io/m4",
            "mjpeg": "https://universalassistant.io/mjpeg",
            "ustream": "https://universalassistant.io/ustream",
        },
        "feeds": {
            "blog": {"url": "https://universalassistant.io/blog"},
            "wiki": {"type": "mediawiki", "url": "https://universalassistant.io/wiki"},
            "calendar": {"type": "ical", "url": "https://universalassistant.io/calendar"},
            "flicker": {"url": "https://www.flickr.com/photos/universal-assistant"},
        },
        "cache": {"schedule": "m.02"},
        "projects": [
            "https://universalassistant.io/projects/1",
            "https://universalassistant.io/projects/2",
            "https://universalassistant.io/projects/3",
        ],
        "radio_show": [
            {
                "name": "Radioshow",
                "url": "https://universalassistant.io/radio",
                "type": "ogg",
                "start": "2019-09-02T10:00Z",
                "end": "2019-09-02T12:00Z",
            }
        ],
    }
}

SENSOR_OUTPUT = {
    "temperature": [
        {
            "location": "Home",
            "name": "temp1",
            "unit": UnitOfTemperature.CELSIUS,
            "value": 25.0,
        },
        {
            "location": "outside",
            "name": "temp2",
            "unit": UnitOfTemperature.CELSIUS,
            "value": 23.0,
        },
        {
            "location": "Home",
            "name": "temp3",
            "unit": UnitOfTemperature.CELSIUS,
            "value": None,
        },
    ],
    "humidity": [
        {"location": "Home", "name": "hum1", "unit": PERCENTAGE, "value": 88.0}
    ],
}


@pytest.fixture
async def mock_client(
    hass: UniversalAssistant, hass_client: ClientSessionGenerator
) -> TestClient:
    """Start the Universal Universal Home Assistant HTTP component."""
    await async_setup_component(hass, DOMAIN, CONFIG)

    hass.states.async_set(
        "test.temp1",
        25,
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.temp2",
        23,
        attributes={
            ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS,
            ATTR_SENSOR_LOCATION: "outside",
        },
    )
    hass.states.async_set(
        "test.temp3",
        "foo",
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.temp3",
        "foo",
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.hum1", 88, attributes={ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE}
    )

    return await hass_client()


async def test_spaceapi_get(hass: UniversalAssistant, mock_client: TestClient) -> None:
    """Test response after start-up Universal Universal Home Assistant."""
    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()

    assert data["api"] == SPACEAPI_VERSION
    assert data["space"] == "Home"
    assert data["contact"]["email"] == "hello@universalassistant.io"
    assert data["location"]["address"] == "In your Home"
    assert data["location"]["lat"] == 32.87336
    assert data["location"]["lon"] == -117.22743
    assert data["state"]["open"] == "null"
    assert data["state"]["icon"]["open"] == "https://universalassistant.io/open.png"
    assert data["state"]["icon"]["closed"] == "https://universalassistant.io/close.png"
    assert data["spacefed"]["spacenet"] == bool(1)
    assert data["spacefed"]["spacesaml"] == bool(0)
    assert data["spacefed"]["spacephone"] == bool(1)
    assert data["cam"][0] == "https://universalassistant.io/cam1"
    assert data["cam"][1] == "https://universalassistant.io/cam2"
    assert data["stream"]["m4"] == "https://universalassistant.io/m4"
    assert data["stream"]["mjpeg"] == "https://universalassistant.io/mjpeg"
    assert data["stream"]["ustream"] == "https://universalassistant.io/ustream"
    assert data["feeds"]["blog"]["url"] == "https://universalassistant.io/blog"
    assert data["feeds"]["wiki"]["type"] == "mediawiki"
    assert data["feeds"]["wiki"]["url"] == "https://universalassistant.io/wiki"
    assert data["feeds"]["calendar"]["type"] == "ical"
    assert data["feeds"]["calendar"]["url"] == "https://universalassistant.io/calendar"
    assert (
        data["feeds"]["flicker"]["url"]
        == "https://www.flickr.com/photos/universal-assistant"
    )
    assert data["cache"]["schedule"] == "m.02"
    assert data["projects"][0] == "https://universalassistant.io/projects/1"
    assert data["projects"][1] == "https://universalassistant.io/projects/2"
    assert data["projects"][2] == "https://universalassistant.io/projects/3"
    assert data["radio_show"][0]["name"] == "Radioshow"
    assert data["radio_show"][0]["url"] == "https://universalassistant.io/radio"
    assert data["radio_show"][0]["type"] == "ogg"
    assert data["radio_show"][0]["start"] == "2019-09-02T10:00Z"
    assert data["radio_show"][0]["end"] == "2019-09-02T12:00Z"


async def test_spaceapi_state_get(hass: UniversalAssistant, mock_client: TestClient) -> None:
    """Test response if the state entity was set."""
    hass.states.async_set("test.test_door", True)

    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert data["state"]["open"] == bool(1)


async def test_spaceapi_sensors_get(
    hass: UniversalAssistant, mock_client: TestClient
) -> None:
    """Test the response for the sensors."""
    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert data["sensors"] == SENSOR_OUTPUT


async def test_spaceapi_no_auth_required(
    hass: UniversalAssistant, hass_client_no_auth: ClientSessionGenerator
) -> None:
    """Test SpaceAPI is accessible without authentication."""
    assert await async_setup_component(hass, DOMAIN, CONFIG)

    hass.states.async_set("test.test_door", "on")

    client = await hass_client_no_auth()
    resp = await client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert data["space"] == "Home"


async def test_spaceapi_cors_headers(
    hass: UniversalAssistant, hass_client_no_auth: ClientSessionGenerator
) -> None:
    """Test CORS headers are present on SpaceAPI responses."""
    assert await async_setup_component(hass, DOMAIN, CONFIG)

    hass.states.async_set("test.test_door", "on")

    client = await hass_client_no_auth()
    resp = await client.options(
        URL_API_SPACEAPI,
        headers={
            "origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.headers["Access-Control-Allow-Origin"] == "http://example.com"
    assert "GET" in resp.headers["Access-Control-Allow-Methods"]
