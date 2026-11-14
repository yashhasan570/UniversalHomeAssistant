"""Support for the Abode Security System."""

from enum import StrEnum
from typing import TYPE_CHECKING

from jaraco.abode.exceptions import Exception as AbodeException
import probatio

from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__, ServiceCall, callback
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import config_validation as cv, service
from universalassistant.helpers.dispatcher import dispatcher_send

from .const import DOMAIN

if TYPE_CHECKING:
    from . import AbodeConfigEntry, AbodeSystem


class AbodeService(StrEnum):
    """Store keys for Abode services."""

    CAPTURE_IMAGE = "capture_image"
    CHANGE_SETTING = "change_setting"
    TRIGGER_AUTOMATION = "trigger_automation"


class AbodeServiceArgument(StrEnum):
    """Store keys for Abode service arguments."""

    SETTING = "setting"
    VALUE = "value"


CHANGE_SETTING_SCHEMA = probatio.Schema(
    {
        probatio.Required(AbodeServiceArgument.SETTING): cv.string,
        probatio.Required(AbodeServiceArgument.VALUE): cv.string,
    }
)

CAPTURE_IMAGE_SCHEMA = probatio.Schema({CommonServiceArgument.ENTITY_ID: cv.entity_ids})

AUTOMATION_SCHEMA = probatio.Schema({CommonServiceArgument.ENTITY_ID: cv.entity_ids})


def _get_abode_system(hass: __HAC_KEEP__) -> AbodeSystem:
    """Return the Abode system for the loaded config entry."""
    entry: AbodeConfigEntry = service.async_get_config_entry(hass, DOMAIN, None)
    return entry.runtime_data


def _change_setting(call: ServiceCall) -> None:
    """Change an Abode system setting."""
    setting = call.data[AbodeServiceArgument.SETTING]
    value = call.data[AbodeServiceArgument.VALUE]

    try:
        _get_abode_system(call.hass).abode.set_setting(setting, value)
    except AbodeException as ex:
        raise __HAC_KEEP__Error(
            translation_domain=DOMAIN,
            translation_key="change_setting_failed",
            translation_placeholders={"error": str(ex)},
        ) from ex


def _capture_image(call: ServiceCall) -> None:
    """Capture a new image."""
    entity_ids = call.data[CommonServiceArgument.ENTITY_ID]

    target_entities = [
        entity_id
        for entity_id in _get_abode_system(call.hass).entity_ids
        if entity_id in entity_ids
    ]

    for entity_id in target_entities:
        signal = f"abode_camera_capture_{entity_id}"
        dispatcher_send(call.hass, signal)


def _trigger_automation(call: ServiceCall) -> None:
    """Trigger an Abode automation."""
    entity_ids = call.data[CommonServiceArgument.ENTITY_ID]

    target_entities = [
        entity_id
        for entity_id in _get_abode_system(call.hass).entity_ids
        if entity_id in entity_ids
    ]

    for entity_id in target_entities:
        signal = f"abode_trigger_automation_{entity_id}"
        dispatcher_send(call.hass, signal)


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """__HA_KEEP__ services."""

    hass.services.async_register(
        DOMAIN,
        AbodeService.CHANGE_SETTING,
        _change_setting,
        schema=CHANGE_SETTING_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN, AbodeService.CAPTURE_IMAGE, _capture_image, schema=CAPTURE_IMAGE_SCHEMA
    )

    hass.services.async_register(
        DOMAIN,
        AbodeService.TRIGGER_AUTOMATION,
        _trigger_automation,
        schema=AUTOMATION_SCHEMA,
    )
