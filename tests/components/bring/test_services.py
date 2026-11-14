"""Test actions of Bring! integration."""

from unittest.mock import AsyncMock

from bring_api import (
    ActivityType,
    BringActivityResponse,
    BringNotificationType,
    BringRequestException,
    ReactionType,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.bring.const import DOMAIN
from universalassistant.components.bring.services import BringService, BringServiceArgument
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import entity_registry as er


@pytest.mark.parametrize(
    ("reaction", "call_arg"),
    [
        ("drooling", ReactionType.DROOLING),
        ("heart", ReactionType.HEART),
        ("monocle", ReactionType.MONOCLE),
        ("thumbs_up", ReactionType.THUMBS_UP),
    ],
)
async def test_send_reaction(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    mock_bring_client: AsyncMock,
    reaction: str,
    call_arg: ReactionType,
) -> None:
    """Test send activity stream reaction."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    await hass.services.async_call(
        DOMAIN,
        BringService.SEND_REACTION,
        service_data={
            CommonServiceArgument.ENTITY_ID: "event.einkauf_activities",
            BringServiceArgument.REACTION: reaction,
        },
        blocking=True,
    )

    mock_bring_client.notify.assert_called_once_with(
        "e542eef6-dba7-4c31-a52c-29e6ab9d83a5",
        BringNotificationType.LIST_ACTIVITY_STREAM_REACTION,
        receiver="9a21fdfc-63a4-441a-afc1-ef3030605a9d",
        activity="673594a9-f92d-4cb6-adf1-d2f7a83207a4",
        activity_type=ActivityType.LIST_ITEMS_CHANGED,
        reaction=call_arg,
    )


async def test_send_reaction_exception(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    mock_bring_client: AsyncMock,
) -> None:
    """Test send activity stream reaction with exception."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED
    mock_bring_client.notify.side_effect = BringRequestException
    with pytest.raises(__HAC_KEEP__Error) as err:
        await hass.services.async_call(
            DOMAIN,
            BringService.SEND_REACTION,
            service_data={
                CommonServiceArgument.ENTITY_ID: "event.einkauf_activities",
                BringServiceArgument.REACTION: "heart",
            },
            blocking=True,
        )
    assert err.value.translation_key == "reaction_request_failed"


@pytest.mark.usefixtures("mock_bring_client")
async def test_send_reaction_config_entry_not_loaded(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
) -> None:
    """Test send activity stream reaction config entry not loaded exception."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert await hass.config_entries.async_unload(bring_config_entry.entry_id)

    assert bring_config_entry.state is ConfigEntryState.NOT_LOADED

    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            BringService.SEND_REACTION,
            service_data={
                CommonServiceArgument.ENTITY_ID: "event.einkauf_activities",
                BringServiceArgument.REACTION: "heart",
            },
            blocking=True,
        )
    assert err.value.translation_key == "service_config_entry_not_loaded"
    assert err.value.translation_placeholders["entry_title"] == "Mock Title"


@pytest.mark.usefixtures("mock_bring_client")
async def test_send_reaction_unknown_entity(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test send activity stream reaction unknown entity exception."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    entity_registry.async_update_entity(
        "event.einkauf_activities", disabled_by=er.RegistryEntryDisabler.USER
    )
    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            BringService.SEND_REACTION,
            service_data={
                CommonServiceArgument.ENTITY_ID: "event.einkauf_activities",
                BringServiceArgument.REACTION: "heart",
            },
            blocking=True,
        )

    assert err.value.translation_key == "entity_not_found"
    assert err.value.translation_placeholders == {
        "entity_id": "event.einkauf_activities"
    }


async def test_send_reaction_not_found(
    hass: __HAC_KEEP__,
    bring_config_entry: MockConfigEntry,
    mock_bring_client: AsyncMock,
) -> None:
    """Test send activity stream reaction not found validation error."""
    mock_bring_client.get_activity.return_value = BringActivityResponse.from_dict(
        {"timeline": [], "timestamp": "2025-01-01T03:09:33.036Z", "totalEvents": 0}
    )

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    with pytest.raises(__HAC_KEEP__Error) as err:
        await hass.services.async_call(
            DOMAIN,
            BringService.SEND_REACTION,
            service_data={
                CommonServiceArgument.ENTITY_ID: "event.einkauf_activities",
                BringServiceArgument.REACTION: "heart",
            },
            blocking=True,
        )
    assert err.value.translation_key == "activity_not_found"
