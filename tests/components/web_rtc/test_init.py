"""Test the WebRTC integration."""

from pytest_universalassistant.typing import WebSocketGenerator
from webrtc_models import RTCIceServer

from universalassistant.components.web_rtc import (
    DOMAIN,
    async_get_ice_servers,
    async_register_ice_servers,
)
from universalassistant.core import UniversalAssistant, callback
from universalassistant.core_config import async_process_ha_core_config
from universalassistant.setup import async_setup_component


async def test_async_setup(hass: UniversalAssistant) -> None:
    """Test setting up the web_rtc integration."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    # Verify default ICE servers are registered
    ice_servers = async_get_ice_servers(hass)
    assert len(ice_servers) == 1
    assert ice_servers[0].urls == [
        "stun:stun.universalassistant.io:3478",
        "stun:stun.universalassistant.io:80",
    ]


async def test_async_setup_custom_ice_servers_core(hass: UniversalAssistant) -> None:
    """Test setting up web_rtc with custom ICE servers in config."""
    await async_process_ha_core_config(
        hass,
        {"webrtc": {"ice_servers": [{"url": "stun:custom_stun_server:3478"}]}},
    )

    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    ice_servers = async_get_ice_servers(hass)
    assert len(ice_servers) == 1
    assert ice_servers[0].urls == ["stun:custom_stun_server:3478"]


async def test_async_setup_custom_ice_servers_integration(hass: UniversalAssistant) -> None:
    """Test setting up web_rtc with custom ICE servers in config."""
    assert await async_setup_component(
        hass,
        DOMAIN,
        {
            "web_rtc": {
                "ice_servers": [
                    {"url": "stun:custom_stun_server:3478"},
                    {
                        "url": "stun:custom_stun_server:3478",
                        "credential": "mock-credential",
                    },
                    {
                        "url": "stun:custom_stun_server:3478",
                        "username": "mock-username",
                    },
                    {
                        "url": "stun:custom_stun_server:3478",
                        "credential": "mock-credential",
                        "username": "mock-username",
                    },
                ]
            }
        },
    )
    await hass.async_block_till_done()

    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == [
        RTCIceServer(
            urls=["stun:custom_stun_server:3478"],
        ),
        RTCIceServer(
            urls=["stun:custom_stun_server:3478"],
            credential="mock-credential",
        ),
        RTCIceServer(
            urls=["stun:custom_stun_server:3478"],
            username="mock-username",
        ),
        RTCIceServer(
            urls=["stun:custom_stun_server:3478"],
            username="mock-username",
            credential="mock-credential",
        ),
    ]


async def test_async_setup_custom_ice_servers_core_and_integration(
    hass: UniversalAssistant,
) -> None:
    """Test setting up web_rtc with custom ICE servers in config."""
    await async_process_ha_core_config(
        hass,
        {"webrtc": {"ice_servers": [{"url": "stun:custom_stun_server_core:3478"}]}},
    )

    assert await async_setup_component(
        hass,
        DOMAIN,
        {
            "web_rtc": {
                "ice_servers": [{"url": "stun:custom_stun_server_integration:3478"}]
            }
        },
    )
    await hass.async_block_till_done()

    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == [
        RTCIceServer(
            urls=["stun:custom_stun_server_core:3478"],
        ),
        RTCIceServer(
            urls=["stun:custom_stun_server_integration:3478"],
        ),
    ]


async def test_async_register_ice_servers(hass: UniversalAssistant) -> None:
    """Test registering ICE servers."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    default_servers = async_get_ice_servers(hass)

    called = 0

    @callback
    def get_ice_servers() -> list[RTCIceServer]:
        nonlocal called
        called += 1
        return [
            RTCIceServer(urls="stun:example.com"),
            RTCIceServer(urls="turn:example.com"),
        ]

    unregister = async_register_ice_servers(hass, get_ice_servers)
    assert called == 0

    # Getting ice servers should call the callback
    ice_servers = async_get_ice_servers(hass)
    assert called == 1
    assert ice_servers == [
        *default_servers,
        RTCIceServer(urls="stun:example.com"),
        RTCIceServer(urls="turn:example.com"),
    ]

    # Unregister and verify servers are removed
    unregister()
    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == default_servers


async def test_multiple_ice_server_registrations(hass: UniversalAssistant) -> None:
    """Test registering multiple ICE server providers."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    default_servers = async_get_ice_servers(hass)

    @callback
    def get_ice_servers_1() -> list[RTCIceServer]:
        return [RTCIceServer(urls="stun:server1.com")]

    @callback
    def get_ice_servers_2() -> list[RTCIceServer]:
        return [
            RTCIceServer(
                urls=["stun:server2.com", "turn:server2.com"],
                username="user",
                credential="pass",
            )
        ]

    unregister_1 = async_register_ice_servers(hass, get_ice_servers_1)
    unregister_2 = async_register_ice_servers(hass, get_ice_servers_2)

    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == [
        *default_servers,
        RTCIceServer(urls="stun:server1.com"),
        RTCIceServer(
            urls=["stun:server2.com", "turn:server2.com"],
            username="user",
            credential="pass",
        ),
    ]

    # Unregister first provider
    unregister_1()
    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == [
        *default_servers,
        RTCIceServer(
            urls=["stun:server2.com", "turn:server2.com"],
            username="user",
            credential="pass",
        ),
    ]

    # Unregister second provider
    unregister_2()
    ice_servers = async_get_ice_servers(hass)
    assert ice_servers == default_servers


async def test_ws_ice_servers_with_registered_servers(
    hass: UniversalAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """Test WebSocket ICE servers endpoint with registered servers."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    @callback
    def get_ice_server() -> list[RTCIceServer]:
        return [
            RTCIceServer(
                urls=["stun:example2.com", "turn:example2.com"],
                username="user",
                credential="pass",
            )
        ]

    async_register_ice_servers(hass, get_ice_server)

    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "web_rtc/ice_servers"})
    msg = await client.receive_json()

    # Assert WebSocket response includes registered ICE servers
    assert msg["type"] == "result"
    assert msg["success"]
    assert msg["result"] == [
        {
            "urls": [
                "stun:stun.universalassistant.io:3478",
                "stun:stun.universalassistant.io:80",
            ]
        },
        {
            "urls": ["stun:example2.com", "turn:example2.com"],
            "username": "user",
            "credential": "pass",
        },
    ]
