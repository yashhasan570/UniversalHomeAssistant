"""Load fixtures while collecting a consuming project's conftest."""

from pytest_universalassistant.common import load_json_object_fixture

assert load_json_object_fixture("sample.json") == {"state": "ready"}
