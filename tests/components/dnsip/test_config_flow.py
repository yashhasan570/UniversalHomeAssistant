"""Test the DNS IP config flow."""

from unittest.mock import patch

from aiodns.error import DNSError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.dnsip.config_flow import DATA_SCHEMA
from universalassistant.components.dnsip.const import (
    CONF_ADDITIONAL_OPTIONS,
    CONF_HOSTNAME,
    CONF_IPV4,
    CONF_IPV6,
    CONF_PORT_IPV6,
    CONF_RESOLVER,
    CONF_RESOLVER_IPV6,
    DEFAULT_HOSTNAME,
    DOMAIN,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_NAME, CONF_PORT
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

from . import RetrieveDNS


async def test_form(hass: UniversalAssistant) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["data_schema"] == DATA_SCHEMA
    assert result["errors"] == {}

    with (
        patch(
            "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
            return_value=RetrieveDNS(),
        ),
        patch(
            "universalassistant.components.dnsip.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOSTNAME: "universalassistant.io", CONF_ADDITIONAL_OPTIONS: {}},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "universalassistant.io"
    assert result2["data"] == {
        "hostname": "universalassistant.io",
        "name": "universalassistant.io",
        "ipv4": True,
        "ipv6": True,
    }
    assert result2["options"] == {
        "resolver": "208.67.222.222",
        "resolver_ipv6": "2620:119:53::53",
        "port": 53,
        "port_ipv6": 53,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_with_additional_options(hass: UniversalAssistant) -> None:
    """Test we can submit the form with custom resolver and port options."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    assert result["data_schema"] == DATA_SCHEMA

    with (
        patch(
            "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
            return_value=RetrieveDNS(),
        ),
        patch(
            "universalassistant.components.dnsip.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOSTNAME: "universalassistant.io",
                CONF_ADDITIONAL_OPTIONS: {
                    CONF_RESOLVER: "8.8.8.8",
                    CONF_RESOLVER_IPV6: "2620:119:53::53",
                    CONF_PORT: 53,
                    CONF_PORT_IPV6: 53,
                },
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "universalassistant.io"
    assert result2["data"] == {
        "hostname": "universalassistant.io",
        "name": "universalassistant.io",
        "ipv4": True,
        "ipv6": True,
    }
    assert result2["options"] == {
        "resolver": "8.8.8.8",
        "resolver_ipv6": "2620:119:53::53",
        "port": 53,
        "port_ipv6": 53,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_error(hass: UniversalAssistant) -> None:
    """Test validate url fails."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        side_effect=DNSError("Did not find"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOSTNAME: "universalassistant.io",
                CONF_ADDITIONAL_OPTIONS: {},
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "user"
    assert result2["errors"] == {"base": "invalid_hostname"}

    with (
        patch(
            "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
            return_value=RetrieveDNS(),
        ),
        patch(
            "universalassistant.components.dnsip.async_setup_entry",
            return_value=None,
        ),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOSTNAME: "universalassistant.io",
                CONF_ADDITIONAL_OPTIONS: {},
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_flow_already_exist(hass: UniversalAssistant) -> None:
    """Test flow when unique id already exist."""

    MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: True,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::5",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        unique_id="universalassistant.io",
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    dns_mock = RetrieveDNS()
    with (
        patch(
            "universalassistant.components.dnsip.async_setup_entry",
            return_value=None,
        ),
        patch(
            "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
            return_value=dns_mock,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOSTNAME: "universalassistant.io",
                CONF_ADDITIONAL_OPTIONS: {},
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


async def test_options_flow(hass: UniversalAssistant) -> None:
    """Test options config flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="12345",
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::5",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={
                CONF_RESOLVER: "8.8.8.8",
                CONF_RESOLVER_IPV6: "2001:4860:4860::8888",
                CONF_PORT: 53,
                CONF_PORT_IPV6: 53,
            },
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "resolver": "8.8.8.8",
        "resolver_ipv6": "2001:4860:4860::8888",
        "port": 53,
        "port_ipv6": 53,
    }

    assert entry.state is ConfigEntryState.LOADED


async def test_options_flow_empty_return(hass: UniversalAssistant) -> None:
    """Test options config flow with empty return from user."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="12345",
        data={
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "8.8.8.8",
            CONF_RESOLVER_IPV6: "2620:119:53::1",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "resolver": "208.67.222.222",
        "resolver_ipv6": "2620:119:53::53",
        "port": 53,
        "port_ipv6": 53,
    }

    entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert entry.data == {
        "hostname": "universalassistant.io",
        "ipv4": True,
        "ipv6": False,
        "name": "universalassistant.io",
    }
    assert entry.options == {
        "resolver": "208.67.222.222",
        "resolver_ipv6": "2620:119:53::53",
        "port": 53,
        "port_ipv6": 53,
    }


@pytest.mark.parametrize(
    "p_input",
    [
        {
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::5",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        {
            CONF_HOSTNAME: "universalassistant.io",
            CONF_NAME: "universalassistant.io",
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::5",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
            CONF_IPV4: False,
            CONF_IPV6: True,
        },
    ],
)
async def test_options_error(hass: UniversalAssistant, p_input: dict[str, str]) -> None:
    """Test validate url fails in options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="12345",
        data=p_input,
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.async_setup_entry",
        return_value=None,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        side_effect=DNSError("Did not find"),
    ):
        result2 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {
                CONF_RESOLVER: "192.168.200.34",
                CONF_RESOLVER_IPV6: "2001:4860:4860::8888",
                CONF_PORT: 53,
                CONF_PORT_IPV6: 53,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "init"
    if p_input[CONF_IPV4]:
        assert result2["errors"] == {"resolver": "invalid_resolver"}
    if p_input[CONF_IPV6]:
        assert result2["errors"] == {"resolver_ipv6": "invalid_resolver"}

    with (
        patch(
            "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
            return_value=RetrieveDNS(),
        ),
        patch(
            "universalassistant.components.dnsip.async_setup_entry",
            return_value=None,
        ),
    ):
        result3 = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {
                CONF_RESOLVER: "192.168.200.34",
                CONF_RESOLVER_IPV6: "2001:4860:4860::8888",
                CONF_PORT: 53,
                CONF_PORT_IPV6: 53,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_cannot_configure_options_for_myip(hass: UniversalAssistant) -> None:
    """Test options config flow aborts for default myip hostname."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="12345",
        data={
            CONF_HOSTNAME: DEFAULT_HOSTNAME,
            CONF_NAME: "myip",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::5",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_options"
