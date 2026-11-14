"""Test the swiss_public_transport service."""

import logging
from unittest.mock import AsyncMock, patch

from opendata_transport.exceptions import (
    OpendataTransportConnectionError,
    OpendataTransportError,
)
import probatio
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_load_json_array_fixture

from universalassistant.components.swiss_public_transport.const import (
    CONF_DESTINATION,
    CONF_START,
    CONNECTIONS_COUNT,
    CONNECTIONS_MAX,
    DOMAIN,
)
from universalassistant.components.swiss_public_transport.helper import unique_id_from_config
from universalassistant.components.swiss_public_transport.services import (
    SwissPublicTransportService,
    SwissPublicTransportServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError

from . import setup_integration

_LOGGER = logging.getLogger(__name__)

MOCK_DATA_STEP_BASE = {
    CONF_START: "test_start",
    CONF_DESTINATION: "test_destination",
}


@pytest.mark.parametrize(
    ("data", "config_data"),
    [
        ({SwissPublicTransportServiceArgument.LIMIT: 1}, MOCK_DATA_STEP_BASE),
        ({SwissPublicTransportServiceArgument.LIMIT: 2}, MOCK_DATA_STEP_BASE),
        ({SwissPublicTransportServiceArgument.LIMIT: 3}, MOCK_DATA_STEP_BASE),
        (
            {SwissPublicTransportServiceArgument.LIMIT: CONNECTIONS_MAX},
            MOCK_DATA_STEP_BASE,
        ),
        ({}, MOCK_DATA_STEP_BASE),
    ],
)
async def test_service_call_fetch_connections_success(
    hass: UniversalAssistant,
    data: dict,
    config_data,
) -> None:
    """Test the fetch_connections service."""

    unique_id = unique_id_from_config(config_data)

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=config_data,
        title=f"Service test call with data={data}",
        unique_id=unique_id,
        entry_id=f"entry_{unique_id}",
    )

    with patch(
        "universalassistant.components.swiss_public_transport.OpendataTransport",
        return_value=AsyncMock(),
    ) as mock:
        mock().connections = (
            await async_load_json_array_fixture(hass, "connections.json", DOMAIN)
        )[
            0 : data.get(SwissPublicTransportServiceArgument.LIMIT, CONNECTIONS_COUNT)
            + 2
        ]

        await setup_integration(hass, config_entry)

        data[CommonServiceArgument.CONFIG_ENTRY_ID] = config_entry.entry_id
        assert hass.services.has_service(
            DOMAIN, SwissPublicTransportService.FETCH_CONNECTIONS
        )
        response = await hass.services.async_call(
            domain=DOMAIN,
            service=SwissPublicTransportService.FETCH_CONNECTIONS,
            service_data=data,
            blocking=True,
            return_response=True,
        )
        await hass.async_block_till_done()
        assert response["connections"] is not None
        assert len(response["connections"]) == data.get(
            SwissPublicTransportServiceArgument.LIMIT, CONNECTIONS_COUNT
        )


@pytest.mark.parametrize(
    ("limit", "config_data", "expected_result", "raise_error"),
    [
        (-1, MOCK_DATA_STEP_BASE, pytest.raises(probatio.error.MultipleInvalid), None),
        (0, MOCK_DATA_STEP_BASE, pytest.raises(probatio.error.MultipleInvalid), None),
        (
            CONNECTIONS_MAX + 1,
            MOCK_DATA_STEP_BASE,
            pytest.raises(probatio.error.MultipleInvalid),
            None,
        ),
        (
            1,
            MOCK_DATA_STEP_BASE,
            pytest.raises(UniversalAssistantError),
            OpendataTransportConnectionError(),
        ),
        (
            2,
            MOCK_DATA_STEP_BASE,
            pytest.raises(UniversalAssistantError),
            OpendataTransportError(),
        ),
    ],
)
async def test_service_call_fetch_connections_error(
    hass: UniversalAssistant,
    limit,
    config_data,
    expected_result,
    raise_error,
) -> None:
    """Test service call with standard error."""

    unique_id = unique_id_from_config(config_data)

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=config_data,
        title=f"Service test call with limit={limit} and error={raise_error}",
        unique_id=unique_id,
        entry_id=f"entry_{unique_id}",
    )

    with patch(
        "universalassistant.components.swiss_public_transport.OpendataTransport",
        return_value=AsyncMock(),
    ) as mock:
        mock().connections = await async_load_json_array_fixture(
            hass, "connections.json", DOMAIN
        )

        await setup_integration(hass, config_entry)

        assert hass.services.has_service(
            DOMAIN, SwissPublicTransportService.FETCH_CONNECTIONS
        )
        mock().async_get_data.side_effect = raise_error
        with expected_result:
            await hass.services.async_call(
                domain=DOMAIN,
                service=SwissPublicTransportService.FETCH_CONNECTIONS,
                service_data={
                    CommonServiceArgument.CONFIG_ENTRY_ID: config_entry.entry_id,
                    SwissPublicTransportServiceArgument.LIMIT: limit,
                },
                blocking=True,
                return_response=True,
            )


async def test_service_call_load_unload(
    hass: UniversalAssistant,
) -> None:
    """Test service call with integration error."""

    unique_id = unique_id_from_config(MOCK_DATA_STEP_BASE)

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_DATA_STEP_BASE,
        title="Service test call for unloaded entry",
        unique_id=unique_id,
        entry_id=f"entry_{unique_id}",
    )

    bad_entry_id = "bad_entry_id"

    with patch(
        "universalassistant.components.swiss_public_transport.OpendataTransport",
        return_value=AsyncMock(),
    ) as mock:
        mock().connections = await async_load_json_array_fixture(
            hass, "connections.json", DOMAIN
        )

        await setup_integration(hass, config_entry)

        assert hass.services.has_service(
            DOMAIN, SwissPublicTransportService.FETCH_CONNECTIONS
        )
        response = await hass.services.async_call(
            domain=DOMAIN,
            service=SwissPublicTransportService.FETCH_CONNECTIONS,
            service_data={
                CommonServiceArgument.CONFIG_ENTRY_ID: config_entry.entry_id,
            },
            blocking=True,
            return_response=True,
        )
        await hass.async_block_till_done()
        assert response["connections"] is not None

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        with pytest.raises(ServiceValidationError) as err:
            await hass.services.async_call(
                domain=DOMAIN,
                service=SwissPublicTransportService.FETCH_CONNECTIONS,
                service_data={
                    CommonServiceArgument.CONFIG_ENTRY_ID: config_entry.entry_id,
                },
                blocking=True,
                return_response=True,
            )
        assert err.value.translation_key == "service_config_entry_not_loaded"

        with pytest.raises(ServiceValidationError) as err:
            await hass.services.async_call(
                domain=DOMAIN,
                service=SwissPublicTransportService.FETCH_CONNECTIONS,
                service_data={
                    CommonServiceArgument.CONFIG_ENTRY_ID: bad_entry_id,
                },
                blocking=True,
                return_response=True,
            )
        assert err.value.translation_key == "service_config_entry_not_found"
