"""Test the webhook component."""

from http import HTTPStatus
from ipaddress import ip_address
from unittest.mock import Mock, patch

from aiohttp import web
from aiohttp.test_utils import TestClient
import pytest
from pytest_universalassistant.typing import ClientSessionGenerator, WebSocketGenerator

from universalassistant.components import webhook
from universalassistant.components.webhook import DOMAIN
from universalassistant.components.websocket_api import auth, http
from universalassistant.core import UniversalAssistant
from universalassistant.core_config import async_process_ha_core_config
from universalassistant.setup import async_setup_component
from universalassistant.util.aiohttp import MockRequest

from tests.test_util import mock_real_ip


@pytest.fixture
async def mock_client(
    hass: UniversalAssistant, hass_client: ClientSessionGenerator
) -> TestClient:
    """Create http client for webhooks."""
    await async_setup_component(hass, DOMAIN, {})
    return await hass_client()


async def test_unregistering_webhook(hass: UniversalAssistant, mock_client) -> None:
    """Test unregistering a webhook."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append(args)

    webhook.async_register(hass, "test", "Test hook", webhook_id, handle)

    resp = await mock_client.post(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1

    webhook.async_unregister(hass, webhook_id)

    resp = await mock_client.post(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1


async def test_generate_webhook_url(hass: UniversalAssistant) -> None:
    """Test we generate a webhook url correctly."""
    await async_process_ha_core_config(
        hass,
        {"external_url": "https://example.com"},
    )
    url = webhook.async_generate_url(hass, "some_id")

    assert url == "https://example.com/api/webhook/some_id"


async def test_generate_webhook_url_internal(hass: UniversalAssistant) -> None:
    """Test we can get the internal URL."""
    await async_process_ha_core_config(
        hass,
        {
            "internal_url": "http://192.168.1.100:8123",
            "external_url": "https://example.com",
        },
    )
    url = webhook.async_generate_url(
        hass, "some_id", allow_external=False, allow_ip=True
    )

    assert url == "http://192.168.1.100:8123/api/webhook/some_id"


async def test_async_generate_path(hass: UniversalAssistant) -> None:
    """Test generating just the path component of the url correctly."""
    path = webhook.async_generate_path("some_id")
    assert path == "/api/webhook/some_id"


async def test_posting_webhook_nonexisting(hass: UniversalAssistant, mock_client) -> None:
    """Test posting to a nonexisting webhook."""
    resp = await mock_client.post("/api/webhook/non-existing")
    assert resp.status == HTTPStatus.OK


async def test_posting_webhook_invalid_json(hass: UniversalAssistant, mock_client) -> None:
    """Test posting to a nonexisting webhook."""
    webhook.async_register(hass, "test", "Test hook", "hello", None)
    resp = await mock_client.post("/api/webhook/hello", data="not-json")
    assert resp.status == HTTPStatus.OK


async def test_posting_webhook_json(hass: UniversalAssistant, mock_client) -> None:
    """Test posting a webhook with JSON data."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append((args[0], args[1], await args[2].text()))

    webhook.async_register(hass, "test", "Test hook", webhook_id, handle)

    resp = await mock_client.post(f"/api/webhook/{webhook_id}", json={"data": True})
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2] == '{"data": true}'


async def test_posting_webhook_no_data(hass: UniversalAssistant, mock_client) -> None:
    """Test posting a webhook with no data."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append(args)

    webhook.async_register(hass, "test", "Test hook", webhook_id, handle)

    resp = await mock_client.post(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2].method == "POST"
    assert await hooks[0][2].text() == ""


async def test_webhook_put(hass: UniversalAssistant, mock_client) -> None:
    """Test sending a put request to a webhook."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append(args)

    webhook.async_register(hass, "test", "Test hook", webhook_id, handle)

    resp = await mock_client.put(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2].method == "PUT"


async def test_webhook_head(hass: UniversalAssistant, mock_client) -> None:
    """Test sending a head request to a webhook."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append(args)

    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, allowed_methods=["HEAD"]
    )

    resp = await mock_client.head(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2].method == "HEAD"

    # Test that status is HTTPStatus.OK even when HEAD is not allowed.
    webhook.async_unregister(hass, webhook_id)
    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, allowed_methods=["PUT"]
    )
    resp = await mock_client.head(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1  # Should not have been called


async def test_webhook_get(hass: UniversalAssistant, mock_client) -> None:
    """Test sending a get request to a webhook."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append(args)

    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, allowed_methods=["GET"]
    )

    resp = await mock_client.get(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2].method == "GET"

    # Test that status is HTTPStatus.METHOD_NOT_ALLOWED even when GET is not allowed.
    webhook.async_unregister(hass, webhook_id)
    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, allowed_methods=["PUT"]
    )
    resp = await mock_client.get(f"/api/webhook/{webhook_id}")
    assert resp.status == HTTPStatus.METHOD_NOT_ALLOWED
    assert len(hooks) == 1  # Should not have been called


async def test_webhook_not_allowed_method(hass: UniversalAssistant) -> None:
    """Test that an exception is raised if an unsupported method is used."""
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        pass

    with pytest.raises(ValueError):
        webhook.async_register(
            hass, "test", "Test hook", webhook_id, handle, allowed_methods=["PATCH"]
        )


async def test_webhook_local_only(hass: UniversalAssistant, mock_client) -> None:
    """Test posting a webhook with local only."""
    hass.config.components.add("cloud")

    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(*args):
        """Handle webhook."""
        hooks.append((args[0], args[1], await args[2].text()))

    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, local_only=True
    )

    resp = await mock_client.post(f"/api/webhook/{webhook_id}", json={"data": True})
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1
    assert hooks[0][0] is hass
    assert hooks[0][1] == webhook_id
    assert hooks[0][2] == '{"data": true}'

    # Request from remote IP
    with patch(
        "universalassistant.components.webhook.ip_address",
        return_value=ip_address("123.123.123.123"),
    ):
        resp = await mock_client.post(f"/api/webhook/{webhook_id}", json={"data": True})
    assert resp.status == HTTPStatus.OK
    # No hook received
    assert len(hooks) == 1

    # Request from Universal Universal Home Assistant Cloud remote UI
    with patch(
        "hass_nabucasa.remote.is_cloud_request", Mock(get=Mock(return_value=True))
    ):
        resp = await mock_client.post(f"/api/webhook/{webhook_id}", json={"data": True})

    # No hook received
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == 1


@pytest.mark.parametrize(
    ("remote", "expected_calls"),
    [
        (None, 0),
        ("123.123.123.123", 0),
        ("not-an-ip", 0),
        ("192.168.1.50", 1),
    ],
)
async def test_webhook_local_only_mock_request(
    hass: UniversalAssistant, remote: str | None, expected_calls: int
) -> None:
    """Test local_only webhooks for MockRequests with various remote values."""
    await async_setup_component(hass, DOMAIN, {})

    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(hass: UniversalAssistant, webhook_id: str, request: web.Request):
        """Handle webhook."""
        hooks.append((hass, webhook_id, await request.text()))

    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, local_only=True
    )

    request = MockRequest(
        content=b'{"data": true}',
        headers={"Content-Type": "application/json"},
        method="POST",
        query_string="",
        mock_source="test",
        remote=remote,
    )
    resp = await webhook.async_handle_webhook(hass, webhook_id, request)
    assert resp.status == HTTPStatus.OK
    assert len(hooks) == expected_calls


async def test_webhook_local_only_supervisor_unix_socket(
    hass: UniversalAssistant, mock_client: TestClient
) -> None:
    """Test local_only webhooks accept requests over the Supervisor Unix socket."""
    hooks = []
    webhook_id = webhook.async_generate_id()

    async def handle(hass: UniversalAssistant, webhook_id: str, request: web.Request):
        """Handle webhook."""
        hooks.append((hass, webhook_id, await request.text()))

    webhook.async_register(
        hass, "test", "Test hook", webhook_id, handle, local_only=True
    )

    # A Unix socket has no peer address, aiohttp reports an empty remote
    with patch(
        "universalassistant.components.webhook.ip_address",
        side_effect=ValueError,
    ):
        resp = await mock_client.post(f"/api/webhook/{webhook_id}", json={"data": True})
        assert resp.status == HTTPStatus.OK
        assert len(hooks) == 0

        with patch(
            "universalassistant.components.webhook.is_supervisor_unix_socket_request",
            return_value=True,
        ):
            resp = await mock_client.post(
                f"/api/webhook/{webhook_id}", json={"data": True}
            )
        assert resp.status == HTTPStatus.OK
        assert len(hooks) == 1
        assert hooks[0][2] == '{"data": true}'


@pytest.mark.usefixtures("enable_custom_integrations")
async def test_listing_webhook(
    hass: UniversalAssistant,
    hass_ws_client: WebSocketGenerator,
    hass_access_token: str,
) -> None:
    """Test unregistering a webhook."""
    assert await async_setup_component(hass, DOMAIN, {})
    client = await hass_ws_client(hass, hass_access_token)

    webhook.async_register(hass, "test", "Test hook", "my-id", None)
    webhook.async_register(
        hass,
        "test",
        "Test hook",
        "my-2",
        None,
        local_only=True,
        allowed_methods=["GET"],
    )

    await client.send_json({"id": 5, "type": "webhook/list"})

    msg = await client.receive_json()
    assert msg["id"] == 5
    assert msg["success"]
    assert msg["result"] == [
        {
            "webhook_id": "my-id",
            "domain": "test",
            "name": "Test hook",
            "local_only": False,
            "allowed_methods": ["POST", "PUT"],
        },
        {
            "webhook_id": "my-2",
            "domain": "test",
            "name": "Test hook",
            "local_only": True,
            "allowed_methods": ["GET"],
        },
    ]


@pytest.mark.usefixtures("enable_custom_integrations")
async def test_listing_webhook_requires_admin(
    hass: UniversalAssistant,
    hass_ws_client: WebSocketGenerator,
    hass_read_only_access_token: str,
) -> None:
    """Test listing webhooks requires an admin user."""
    assert await async_setup_component(hass, DOMAIN, {})
    client = await hass_ws_client(hass, hass_read_only_access_token)

    await client.send_json({"id": 5, "type": "webhook/list"})

    msg = await client.receive_json()
    assert msg["id"] == 5
    assert not msg["success"]
    assert msg["error"]["code"] == "unauthorized"


async def test_ws_webhook(
    hass: UniversalAssistant,
    caplog: pytest.LogCaptureFixture,
    hass_ws_client: WebSocketGenerator,
) -> None:
    """Test sending webhook msg via WS API."""
    assert await async_setup_component(hass, DOMAIN, {})

    received = []

    async def handler(
        hass: UniversalAssistant, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle a webhook."""
        received.append(request)
        return web.json_response({"from": "handler"})

    webhook.async_register(hass, "test", "Test", "mock-webhook-id", handler)

    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 5,
            "type": "webhook/handle",
            "webhook_id": "mock-webhook-id",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": '{"hello": "world"}',
            "query": "a=2",
        }
    )

    result = await client.receive_json()
    assert result["success"], result
    assert result["result"] == {
        "status": 200,
        "body": '{"from": "handler"}',
        "headers": {"Content-Type": "application/json"},
    }

    assert len(received) == 1
    assert received[0].headers["content-type"] == "application/json"
    assert received[0].query == {"a": "2"}
    assert await received[0].json() == {"hello": "world"}
    # The MockRequest is created with the websocket connection's remote IP
    assert received[0].remote is not None

    # Non existing webhook
    caplog.clear()

    await client.send_json(
        {
            "id": 6,
            "type": "webhook/handle",
            "webhook_id": "mock-nonexisting-id",
            "method": "POST",
            "body": '{"nonexisting": "payload"}',
        }
    )

    result = await client.receive_json()
    assert result["success"], result
    assert result["result"] == {
        "status": 200,
        "body": None,
        "headers": {"Content-Type": "application/octet-stream"},
    }

    assert (
        "Received message for unregistered webhook mock-nonexisting-id from webhook/ws"
        in caplog.text
    )
    assert '{"nonexisting": "payload"}' in caplog.text


@pytest.mark.parametrize(
    ("remote_ip", "expected_calls"),
    [
        ("192.168.1.50", 1),
        ("123.123.123.123", 0),
    ],
)
async def test_ws_webhook_local_only(
    hass: UniversalAssistant,
    hass_client_no_auth: ClientSessionGenerator,
    hass_access_token: str,
    remote_ip: str,
    expected_calls: int,
) -> None:
    """Test a local_only webhook over the websocket connection."""
    assert await async_setup_component(hass, DOMAIN, {})
    assert await async_setup_component(hass, "websocket_api", {})
    await hass.async_block_till_done()

    received = []

    async def handler(
        hass: UniversalAssistant, webhook_id: str, request: web.Request
    ) -> web.Response:
        """Handle a webhook."""
        received.append(request)
        return web.json_response({"from": "handler"})

    webhook.async_register(
        hass, "test", "Test", "mock-webhook-id", handler, local_only=True
    )

    set_mock_ip = mock_real_ip(hass.http.app)
    set_mock_ip(remote_ip)

    client = await hass_client_no_auth()

    async with client.ws_connect(http.URL) as ws:
        auth_msg = await ws.receive_json()
        assert auth_msg["type"] == auth.TYPE_AUTH_REQUIRED

        await ws.send_json({"type": auth.TYPE_AUTH, "access_token": hass_access_token})
        auth_msg = await ws.receive_json()
        assert auth_msg["type"] == auth.TYPE_AUTH_OK

        await ws.send_json(
            {
                "id": 5,
                "type": "webhook/handle",
                "webhook_id": "mock-webhook-id",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": '{"hello": "world"}',
                "query": "",
            }
        )
        result = await ws.receive_json()

    assert result["success"], result
    assert result["result"]["status"] == HTTPStatus.OK
    assert len(received) == expected_calls
    if expected_calls:
        assert received[0].remote == remote_ip
