"""Button platform for HDFury Integration."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import override

from hdfury import HDFuryAPI, HDFuryError

from universalassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import HDFuryConfigEntry
from .entity import HDFuryEntity

PARALLEL_UPDATES = 1


@dataclass(kw_only=True, frozen=True)
class HDFuryButtonEntityDescription(ButtonEntityDescription):
    """Description for HDFury button entities."""

    press_fn: Callable[[HDFuryAPI], Awaitable[None]]


BUTTONS: tuple[HDFuryButtonEntityDescription, ...] = (
    HDFuryButtonEntityDescription(
        key="reboot",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.CONFIG,
        press_fn=lambda client: client.issue_reboot(),
    ),
    HDFuryButtonEntityDescription(
        key="issue_hotplug",
        translation_key="issue_hotplug",
        entity_category=EntityCategory.CONFIG,
        press_fn=lambda client: client.issue_hotplug(),
    ),
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: HDFuryConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up buttons using the platform schema."""

    coordinator = entry.runtime_data

    async_add_entities(
        HDFuryButton(coordinator, description) for description in BUTTONS
    )


class HDFuryButton(HDFuryEntity, ButtonEntity):
    """HDFury Button Class."""

    entity_description: HDFuryButtonEntityDescription

    @override
    async def async_press(self) -> None:
        """Handle Button Press."""

        try:
            await self.entity_description.press_fn(self.coordinator.client)
        except HDFuryError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="communication_error",
            ) from error
