"""Fixtures for the tests for the feedreader component."""

import pytest
from pytest_universalassistant.common import async_capture_events, load_fixture_bytes

from universalassistant.components.feedreader.const import DOMAIN
from universalassistant.components.feedreader.coordinator import EVENT_FEEDREADER
from universalassistant.core import Event, __HAC_KEEP__


@pytest.fixture(name="feed_one_event")
def fixture_feed_one_event(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for one event."""
    return load_fixture_bytes("feedreader.xml", DOMAIN)


@pytest.fixture(name="feed_two_event")
def fixture_feed_two_events(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for two event."""
    return load_fixture_bytes("feedreader1.xml", DOMAIN)


@pytest.fixture(name="feed_21_events")
def fixture_feed_21_events(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for twenty one events."""
    return load_fixture_bytes("feedreader2.xml", DOMAIN)


@pytest.fixture(name="feed_three_events")
def fixture_feed_three_events(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for three events."""
    return load_fixture_bytes("feedreader3.xml", DOMAIN)


@pytest.fixture(name="feed_four_events")
def fixture_feed_four_events(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for three events."""
    return load_fixture_bytes("feedreader4.xml", DOMAIN)


@pytest.fixture(name="feed_atom_event")
def fixture_feed_atom_event(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for atom event."""
    return load_fixture_bytes("feedreader5.xml", DOMAIN)


@pytest.fixture(name="feed_identically_timed_events")
def fixture_feed_identically_timed_events(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data for two events published at the exact same time."""
    return load_fixture_bytes("feedreader6.xml", DOMAIN)


@pytest.fixture(name="feed_without_items")
def fixture_feed_without_items(hass: __HAC_KEEP__) -> bytes:
    """Load test feed without any items."""
    return load_fixture_bytes("feedreader7.xml", DOMAIN)


@pytest.fixture(name="feed_only_summary")
def fixture_feed_only_summary(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data with one event containing only a summary, no content."""
    return load_fixture_bytes("feedreader8.xml", DOMAIN)


@pytest.fixture(name="feed_htmlentities")
def fixture_feed_htmlentities(hass: __HAC_KEEP__) -> bytes:
    """Load test feed data with HTML Entities."""
    return load_fixture_bytes("feedreader9.xml", DOMAIN)


@pytest.fixture(name="feed_atom_htmlentities")
def fixture_feed_atom_htmlentities(hass: __HAC_KEEP__) -> bytes:
    """Load test ATOM feed data with HTML Entities."""
    return load_fixture_bytes("feedreader10.xml", DOMAIN)


@pytest.fixture(name="feed_unsorted")
def fixture_feed_unsorted(hass: __HAC_KEEP__) -> bytes:
    """Load test ATOM feed data with HTML Entities."""
    return load_fixture_bytes("feedreader11.xml", DOMAIN)


@pytest.fixture(name="feed_unsorted_update")
def fixture_feed_unsorted_update(hass: __HAC_KEEP__) -> bytes:
    """Load test ATOM feed data with HTML Entities."""
    return load_fixture_bytes("feedreader12.xml", DOMAIN)


@pytest.fixture(name="events")
async def fixture_events(hass: __HAC_KEEP__) -> list[Event]:
    """Fixture that catches alexa events."""
    return async_capture_events(hass, EVENT_FEEDREADER)
