"""The tests for the person component."""

import logging
from typing import Any

import pytest
from pytest_universalassistant.common import MockUser

from universalassistant.components import person
from universalassistant.components.person import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import collection
from universalassistant.setup import async_setup_component

DEVICE_TRACKER = "device_tracker.test_tracker"
DEVICE_TRACKER_2 = "device_tracker.test_tracker_2"


@pytest.fixture
def storage_collection(hass: __HAC_KEEP__) -> person.PersonStorageCollection:
    """Return an empty storage collection."""
    id_manager = collection.IDManager()
    return person.PersonStorageCollection(
        person.PersonStore(hass, person.STORAGE_VERSION, person.STORAGE_KEY),
        id_manager,
        collection.YamlCollection(
            logging.getLogger(f"{person.__name__}.yaml_collection"), id_manager
        ),
    )


@pytest.fixture
async def storage_setup(
    hass: __HAC_KEEP__, hass_storage: dict[str, Any], hass_admin_user: MockUser
) -> None:
    """Storage setup."""
    hass_storage[DOMAIN] = {
        "key": DOMAIN,
        "version": 1,
        "data": {
            "persons": [
                {
                    "id": "1234",
                    "name": "tracked person",
                    "user_id": hass_admin_user.id,
                    "device_trackers": [DEVICE_TRACKER],
                }
            ]
        },
    }
    assert await async_setup_component(hass, DOMAIN, {})
