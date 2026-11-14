"""The test for the DNS IP sensor platform."""

from datetime import timedelta
from unittest.mock import patch

from aiodns.error import DNSError
from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.dnsip.const import (
    CONF_HOSTNAME,
    CONF_IPV4,
    CONF_IPV6,
    CONF_PORT_IPV6,
    CONF_RESOLVER,
    CONF_RESOLVER_IPV6,
    DOMAIN,
)
from universalassistant.components.dnsip.sensor import SCAN_INTERVAL
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_NAME, CONF_PORT, STATE_UNAVAILABLE
from universalassistant.core import __HAC_KEEP__

from . import RetrieveDNS


async def test_sensor(hass: __HAC_KEEP__) -> None:
    """Test the DNS IP sensor."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: True,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        entry_id="1",
        unique_id="universalassistant.io",
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.aiodns.DNSResolver",
        side_effect=[RetrieveDNS(), RetrieveDNS()],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state1 = hass.states.get("sensor.universal_assistant_io")
    state2 = hass.states.get("sensor.universal_assistant_io_ipv6")

    assert state1.state == "1.1.1.1"
    assert state1.attributes["ip_addresses"] == ["1.1.1.1", "1.2.3.4"]
    assert state2.state == "2001:db8::77:dead:beef"
    assert state2.attributes["ip_addresses"] == [
        "2001:db8::77:dead:beef",
        "2001:db8:66::dead:beef",
        "2001:db8:77::dead:beef",
        "2001:db8:77::face:b00c",
    ]


async def test_legacy_sensor(hass: __HAC_KEEP__) -> None:
    """Test the DNS IP sensor configured before the addition of ports."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: True,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
        },
        entry_id="1",
        unique_id="universalassistant.io",
        version=1,
        minor_version=1,
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.aiodns.DNSResolver",
        side_effect=[RetrieveDNS(), RetrieveDNS()],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state1 = hass.states.get("sensor.universal_assistant_io")
    state2 = hass.states.get("sensor.universal_assistant_io_ipv6")

    assert state1.state == "1.1.1.1"
    assert state1.attributes["ip_addresses"] == ["1.1.1.1", "1.2.3.4"]
    assert state2.state == "2001:db8::77:dead:beef"
    assert state2.attributes["ip_addresses"] == [
        "2001:db8::77:dead:beef",
        "2001:db8:66::dead:beef",
        "2001:db8:77::dead:beef",
        "2001:db8:77::face:b00c",
    ]


async def test_sensor_no_response(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Test the DNS IP sensor with DNS error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        entry_id="1",
        unique_id="universalassistant.io",
    )
    entry.add_to_hass(hass)

    dns_mock_ipv4 = RetrieveDNS()
    with patch(
        "universalassistant.components.dnsip.aiodns.DNSResolver",
        return_value=dns_mock_ipv4,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.universal_assistant_io")

    assert state.state == "1.1.1.1"

    dns_mock_ipv4.error = DNSError()
    with patch(
        "universalassistant.components.dnsip.sensor.aiodns.DNSResolver",
        return_value=dns_mock_ipv4,
    ):
        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

        state = hass.states.get("sensor.universal_assistant_io")
        assert state.state == "1.1.1.1"
        assert state.attributes["ip_addresses"] == ["1.1.1.1", "1.2.3.4"]

        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.universal_assistant_io")
    assert state.state == STATE_UNAVAILABLE


async def test_sensor_timeout(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Test the DNS IP sensor with timeout."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        entry_id="1",
        unique_id="universalassistant.io",
    )
    entry.add_to_hass(hass)

    dns_mock_ipv4 = RetrieveDNS()
    with patch(
        "universalassistant.components.dnsip.aiodns.DNSResolver",
        return_value=dns_mock_ipv4,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.universal_assistant_io")

    assert state.state == "1.1.1.1"

    with (
        patch(
            "universalassistant.components.dnsip.sensor.aiodns.DNSResolver",
            return_value=dns_mock_ipv4,
        ),
        patch(
            "universalassistant.components.dnsip.sensor.asyncio.timeout",
            side_effect=TimeoutError(),
        ),
    ):
        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

        state = hass.states.get("sensor.universal_assistant_io")
        assert state.state == "1.1.1.1"
        assert state.attributes["ip_addresses"] == ["1.1.1.1", "1.2.3.4"]

        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

        freezer.tick(timedelta(seconds=SCAN_INTERVAL.seconds))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.universal_assistant_io")
    assert state.state == STATE_UNAVAILABLE


async def test_handle_cname(hass: __HAC_KEEP__) -> None:
    """Test CNAME records are dropped."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        entry_id="1",
        unique_id="universalassistant.io",
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state1 = hass.states.get("sensor.universal_assistant_io")

    assert state1.state == "1.1.1.1"
    assert state1.attributes["ip_addresses"] == ["1.1.1.1", "1.2.3.4"]
