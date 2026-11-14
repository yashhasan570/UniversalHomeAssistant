"""Provider and consumer fixtures independent of transport and device libraries."""

from collections.abc import Awaitable, Callable, Generator
from types import SimpleNamespace
from unittest.mock import Mock, patch

from lorawan_connection import DeviceDescriptor, Unsubscribe
from lorawan_connection.mock import MockConnection
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    MockModule,
    mock_config_flow,
    mock_integration,
    mock_platform,
)

from universalassistant.components.lorawan import DeviceManager, async_register_connection
from universalassistant.config_entries import ConfigEntry, ConfigFlow
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.setup import async_setup_component

from .helpers import ExampleCoordinator, ExampleDevices, ExampleSensor


@pytest.fixture
def mock_connection() -> MockConnection:
    """Use the published in-memory connection."""
    return MockConnection(stack_type="example")


@pytest.fixture(autouse=True)
def connection_integration(
    hass: __HAC_KEEP__, mock_connection: MockConnection
) -> Generator[None]:
    """Mock a connection integration."""

    async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
        entry.async_on_unload(
            await async_register_connection(hass, entry, connection=mock_connection)
        )

    async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
        """Unload a config entry."""

    mock_integration(
        hass,
        MockModule(
            "test_provider",
            dependencies=["lorawan"],
            async_setup_entry=async_setup_entry,
            async_unload_entry=async_unload_entry,
        ),
    )
    mock_platform(hass, "test_provider.config_flow", Mock())
    with mock_config_flow("test_provider", ConfigFlow):
        yield


@pytest.fixture(autouse=True)
def device_integration(hass: __HAC_KEEP__) -> Generator[None]:
    """Mock a device integration with a sensor platform."""

    async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
        manager = entry.runtime_data = DeviceManager(
            hass,
            entry,
            create_collection=ExampleDevices,
            create_coordinator=ExampleCoordinator,
        )
        entry.async_on_unload(manager.close)
        await manager.async_setup()
        await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])

    async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
        await hass.config_entries.async_unload_platforms_or_raise(
            entry, [Platform.SENSOR]
        )

    async def setup_sensor(
        hass: __HAC_KEEP__,
        entry: ConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
    ) -> None:
        @callback
        def added(coordinator: ExampleCoordinator) -> None:
            async_add_entities(
                ExampleSensor(coordinator, key) for key in ("temperature", "humidity")
            )

        entry.async_on_unload(entry.runtime_data.subscribe_coordinator_added(added))

    mock_integration(
        hass,
        MockModule(
            "test_vendor",
            dependencies=["lorawan"],
            async_setup_entry=async_setup_entry,
            async_unload_entry=async_unload_entry,
        ),
    )
    mock_platform(
        hass,
        "test_vendor.sensor",
        SimpleNamespace(async_setup_entry=setup_sensor, PARALLEL_UPDATES=0),
    )
    mock_platform(hass, "test_vendor.config_flow", Mock())
    with (
        mock_config_flow("test_vendor", ConfigFlow),
        patch(
            "universalassistant.components.lorawan.async_get_lorawan",
            return_value={"test_vendor": [("example", 123), ("other_stack", "vendor")]},
        ),
        patch(
            "universalassistant.components.lorawan.connection.discovery_flow.async_create_flow"
        ),
    ):
        yield


@pytest.fixture
def connection_entry(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Create a config entry for the connection integration."""
    entry = MockConfigEntry(domain="test_provider", entry_id="network")
    entry.add_to_hass(hass)
    return entry


type RegisterBackend = Callable[
    [str, list[DeviceDescriptor]], Awaitable[tuple[MockConnection, Unsubscribe]]
]


@pytest.fixture
def registered_backend(hass: __HAC_KEEP__) -> Generator[RegisterBackend]:
    """Register independently controlled connections."""
    cleanups: list[Unsubscribe] = []

    async def register(
        entry_id: str, descriptors: list[DeviceDescriptor]
    ) -> tuple[MockConnection, Unsubscribe]:
        assert await async_setup_component(hass, "lorawan", {})
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry is None:
            entry = MockConfigEntry(domain="test_provider", entry_id=entry_id)
            entry.add_to_hass(hass)
        backend = MockConnection(
            descriptors, stack_type=descriptors[0].stack if descriptors else "example"
        )
        unsubscribe = await async_register_connection(hass, entry, connection=backend)
        cleanups.append(unsubscribe)
        return backend, unsubscribe

    yield register
    for unsubscribe in cleanups:
        unsubscribe()
