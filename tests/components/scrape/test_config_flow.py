"""Test the Scrape config flow."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.rest.data import DEFAULT_TIMEOUT  # pylint: disable=universal-assistant-component-root-import
from universalassistant.components.rest.schema import DEFAULT_METHOD  # pylint: disable=universal-assistant-component-root-import
from universalassistant.components.scrape import DOMAIN
from universalassistant.components.scrape.const import (
    CONF_ADDITIONAL,
    CONF_AUTH,
    CONF_ENCODING,
    CONF_INDEX,
    CONF_SELECT,
    DEFAULT_ENCODING,
    DEFAULT_VERIFY_SSL,
)
from universalassistant.const import (
    CONF_METHOD,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PAYLOAD,
    CONF_RESOURCE,
    CONF_TIMEOUT,
    CONF_USERNAME,
    CONF_VALUE_TEMPLATE,
    CONF_VERIFY_SSL,
)
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.exceptions import UniversalAssistantError

from . import MockRestData


async def test_entry_and_subentry(
    hass: UniversalAssistant, get_data: MockRestData, mock_setup_entry: AsyncMock
) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["step_id"] == "user"
    assert result["type"] is FlowResultType.FORM

    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=get_data,
    ) as mock_data:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: "GET",
                CONF_AUTH: {},
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: True,
                    CONF_TIMEOUT: 10.0,
                },
            },
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["version"] == 3
    assert result["options"] == {
        CONF_RESOURCE: "https://www.universalassistant.io",
        CONF_METHOD: "GET",
        CONF_AUTH: {},
        CONF_ADDITIONAL: {
            CONF_VERIFY_SSL: True,
            CONF_TIMEOUT: 10.0,
            CONF_ENCODING: "UTF-8",
        },
    }

    assert len(mock_data.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1
    await hass.async_block_till_done(wait_background_tasks=True)

    subentry_flows = hass.config_entries.subentries.async_progress()
    assert len(subentry_flows) == 1

    result = await hass.config_entries.subentries.async_configure(
        subentry_flows[0]["flow_id"],
        {
            CONF_NAME: "Current version",
            CONF_INDEX: 0,
            CONF_SELECT: ".current-version h1",
            CONF_ADDITIONAL: {},
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Current version"
    assert result["data"] == {
        CONF_INDEX: 0,
        CONF_SELECT: ".current-version h1",
        CONF_ADDITIONAL: {},
    }


async def test_form_with_post(
    hass: UniversalAssistant, get_data: MockRestData, mock_setup_entry: AsyncMock
) -> None:
    """Test we get the form using POST method."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["step_id"] == "user"
    assert result["type"] is FlowResultType.FORM

    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=get_data,
    ) as mock_data:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: "GET",
                CONF_PAYLOAD: "POST",
                CONF_AUTH: {},
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: True,
                    CONF_TIMEOUT: 10.0,
                },
            },
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["version"] == 3
    assert result["options"] == {
        CONF_RESOURCE: "https://www.universalassistant.io",
        CONF_METHOD: "GET",
        CONF_PAYLOAD: "POST",
        CONF_AUTH: {},
        CONF_ADDITIONAL: {
            CONF_VERIFY_SSL: True,
            CONF_TIMEOUT: 10.0,
            CONF_ENCODING: "UTF-8",
        },
    }

    assert len(mock_data.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("mock_setup_entry")
async def test_flow_fails(hass: UniversalAssistant, get_data: MockRestData) -> None:
    """Test config flow error."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == config_entries.SOURCE_USER

    with patch(
        "universalassistant.components.rest.util.RestData",
        side_effect=UniversalAssistantError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: "GET",
                CONF_AUTH: {},
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: True,
                    CONF_TIMEOUT: 10.0,
                },
            },
        )

    assert result["errors"] == {"base": "resource_error"}

    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=MockRestData("test_scrape_sensor_no_data"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: "GET",
                CONF_AUTH: {},
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: True,
                    CONF_TIMEOUT: 10.0,
                },
            },
        )

    assert result["errors"] == {"base": "no_data"}

    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=get_data,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: "GET",
                CONF_AUTH: {},
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: True,
                    CONF_TIMEOUT: 10.0,
                },
            },
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "https://www.universalassistant.io"
    assert result["options"] == {
        CONF_RESOURCE: "https://www.universalassistant.io",
        CONF_METHOD: "GET",
        CONF_AUTH: {},
        CONF_ADDITIONAL: {
            CONF_VERIFY_SSL: True,
            CONF_TIMEOUT: 10.0,
            CONF_ENCODING: "UTF-8",
        },
    }


async def test_options_resource_flow(
    hass: UniversalAssistant, loaded_entry: MockConfigEntry
) -> None:
    """Test options flow for a resource."""

    state = hass.states.get("sensor.current_version")
    assert state.state == "Current Version: 2021.12.10"

    result = await hass.config_entries.options.async_init(loaded_entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    mocker = MockRestData("test_scrape_sensor2")
    with patch("universalassistant.components.rest.util.RestData", return_value=mocker):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={
                CONF_RESOURCE: "https://www.universalassistant.io",
                CONF_METHOD: DEFAULT_METHOD,
                CONF_AUTH: {
                    CONF_USERNAME: "secret_username",
                    CONF_PASSWORD: "secret_password",
                },
                CONF_ADDITIONAL: {
                    CONF_VERIFY_SSL: DEFAULT_VERIFY_SSL,
                    CONF_TIMEOUT: DEFAULT_TIMEOUT,
                    CONF_ENCODING: DEFAULT_ENCODING,
                },
            },
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_RESOURCE: "https://www.universalassistant.io",
        CONF_METHOD: "GET",
        CONF_AUTH: {
            CONF_USERNAME: "secret_username",
            CONF_PASSWORD: "secret_password",
        },
        CONF_ADDITIONAL: {
            CONF_VERIFY_SSL: True,
            CONF_TIMEOUT: 10.0,
            CONF_ENCODING: "UTF-8",
        },
    }

    await hass.async_block_till_done()

    # Check the entity was updated, no new entity was created
    assert len(hass.states.async_all()) == 1

    # Check the state of the entity has changed as expected
    state = hass.states.get("sensor.current_version")
    assert state.state == "Hidden Version: 2021.12.10"


async def test_reconfigure_sensor_subentry(
    hass: UniversalAssistant, loaded_entry: MockConfigEntry, get_data: MockRestData
) -> None:
    """Test reconfiguring a sensor subentry."""

    state = hass.states.get("sensor.current_version")
    assert state.state == "Current Version: 2021.12.10"

    subentry_id = list(loaded_entry.subentries)[0]

    result = await loaded_entry.start_subentry_reconfigure_flow(
        hass, subentry_id=subentry_id
    )
    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=get_data,
    ):
        result = await hass.config_entries.subentries.async_configure(
            result["flow_id"],
            {
                CONF_ADDITIONAL: {
                    CONF_VALUE_TEMPLATE: "{{ value.split(':')[1] }}",
                },
                CONF_INDEX: 0,
                CONF_SELECT: ".current-version h1",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"

    state = hass.states.get("sensor.current_version")
    assert state.state == "2021.12.10"
