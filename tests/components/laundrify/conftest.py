"""Configure py.test."""

from unittest.mock import AsyncMock, patch

from laundrify_aio import LaundrifyAPI, LaundrifyDevice
import pytest
from pytest_universalassistant.common import MockConfigEntry, load_json_array_fixture
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.laundrify.const import DOMAIN, MANUFACTURER
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import UniversalAssistant

from .const import VALID_ACCESS_TOKEN, VALID_ACCOUNT_ID


@pytest.fixture(name="mock_device")
def laundrify_sensor_fixture() -> LaundrifyDevice:
    """Return a default Laundrify power sensor mock."""
    # Load test data from machines.json
    machine_data = load_json_array_fixture("laundrify/machines.json")[0]

    mock_device = AsyncMock(spec=LaundrifyDevice)
    mock_device.id = machine_data["id"]
    mock_device.manufacturer = MANUFACTURER
    mock_device.model = machine_data["model"]
    mock_device.name = machine_data["name"]
    mock_device.firmwareVersion = machine_data["firmwareVersion"]
    return mock_device


@pytest.fixture(name="laundrify_config_entry")
async def laundrify_setup_config_entry(
    hass: UniversalAssistant,
    laundrify_api_mock,
    access_token: str = VALID_ACCESS_TOKEN,
) -> MockConfigEntry:
    """Create laundrify entry in Universal Home Assistant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=VALID_ACCOUNT_ID,
        data={CONF_ACCESS_TOKEN: access_token},
        minor_version=2,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


@pytest.fixture(name="laundrify_api_mock", autouse=True)
def laundrify_api_fixture(hass_client: ClientSessionGenerator):
    """Mock valid laundrify API responses."""
    with (
        patch(
            "laundrify_aio.LaundrifyAPI.get_account_id",
            return_value=1234,
        ),
        patch(
            "laundrify_aio.LaundrifyAPI.validate_token",
            return_value=True,
        ),
        patch(
            "laundrify_aio.LaundrifyAPI.exchange_auth_code",
            return_value=VALID_ACCESS_TOKEN,
        ),
        patch(
            "laundrify_aio.LaundrifyAPI.get_machines",
            return_value=[
                LaundrifyDevice(machine, LaundrifyAPI)
                for machine in load_json_array_fixture("laundrify/machines.json")
            ],
        ),
    ):
        yield LaundrifyAPI(VALID_ACCESS_TOKEN, hass_client)
