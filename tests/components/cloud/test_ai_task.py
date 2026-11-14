"""Tests for the __HA_KEEP__ Cloud AI Task entity."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from hass_nabucasa.llm import (
    LLMAuthenticationError,
    LLMError,
    LLMImageAttachment,
    LLMRateLimitError,
    LLMResponseError,
    LLMServiceError,
)
from PIL import Image
import probatio
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import ai_task, conversation
from universalassistant.components.cloud import DOMAIN
from universalassistant.components.cloud.ai_task import (
    CloudAITaskEntity,
    async_prepare_image_generation_attachments,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error


@pytest.fixture
def mock_cloud_ai_task_entity(hass: __HAC_KEEP__) -> CloudAITaskEntity:
    """Return a CloudAITaskEntity with a mocked cloud LLM."""
    cloud = MagicMock()
    cloud.llm = MagicMock(
        async_generate_image=AsyncMock(),
        async_edit_image=AsyncMock(),
    )
    cloud.is_logged_in = True
    cloud.valid_subscription = True
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    entity = CloudAITaskEntity(cloud, entry)
    entity.entity_id = "ai_task.cloud_ai_task"
    entity.hass = hass
    return entity


@pytest.fixture(name="mock_handle_chat_log")
def mock_handle_chat_log_fixture() -> AsyncMock:
    """Patch the chat log handler."""
    with patch(
        "universalassistant.components.cloud.ai_task.CloudAITaskEntity._async_handle_chat_log",
        AsyncMock(),
    ) as mock:
        yield mock


@pytest.fixture(name="mock_prepare_generation_attachments")
def mock_prepare_generation_attachments_fixture() -> AsyncMock:
    """Patch image generation attachment preparation."""
    with patch(
        "universalassistant.components.cloud.ai_task.async_prepare_image_generation_attachments",
        AsyncMock(),
    ) as mock:
        yield mock


async def test_prepare_image_generation_attachments(
    hass: __HAC_KEEP__, tmp_path: Path
) -> None:
    """Test preparing attachments for image generation."""
    image_path = tmp_path / "snapshot.jpg"
    Image.new("RGB", (2, 2), "red").save(image_path, "JPEG")

    attachments = [
        conversation.Attachment(
            media_content_id="media-source://media/snapshot.jpg",
            mime_type="image/jpeg",
            path=image_path,
        )
    ]

    result = await async_prepare_image_generation_attachments(hass, attachments)

    assert len(result) == 1
    attachment = result[0]
    assert attachment["filename"] == "snapshot.jpg"
    assert attachment["mime_type"] == "image/png"
    assert attachment["data"].startswith(b"\x89PNG")


async def test_prepare_image_generation_attachments_only_images(
    hass: __HAC_KEEP__, tmp_path: Path
) -> None:
    """Test non image attachments are rejected."""
    doc_path = tmp_path / "context.txt"
    doc_path.write_text("context")

    attachments = [
        conversation.Attachment(
            media_content_id="media-source://media/context.txt",
            mime_type="text/plain",
            path=doc_path,
        )
    ]

    with pytest.raises(
        __HAC_KEEP__Error,
        match="Only image attachments are supported for image generation",
    ):
        await async_prepare_image_generation_attachments(hass, attachments)


async def test_prepare_image_generation_attachments_missing_file(
    hass: __HAC_KEEP__, tmp_path: Path
) -> None:
    """Test missing attachments raise a helpful error."""
    missing_path = tmp_path / "missing.png"

    attachments = [
        conversation.Attachment(
            media_content_id="media-source://media/missing.png",
            mime_type="image/png",
            path=missing_path,
        )
    ]

    with pytest.raises(__HAC_KEEP__Error, match="`.*missing.png` does not exist"):
        await async_prepare_image_generation_attachments(hass, attachments)


async def test_prepare_image_generation_attachments_processing_error(
    hass: __HAC_KEEP__, tmp_path: Path
) -> None:
    """Test invalid image data raises a processing error."""
    broken_path = tmp_path / "broken.png"
    broken_path.write_bytes(b"not-an-image")

    attachments = [
        conversation.Attachment(
            media_content_id="media-source://media/broken.png",
            mime_type="image/png",
            path=broken_path,
        )
    ]

    with pytest.raises(
        __HAC_KEEP__Error,
        match="Failed to process image attachment",
    ):
        await async_prepare_image_generation_attachments(hass, attachments)


async def test_generate_data_returns_text(
    hass: __HAC_KEEP__,
    mock_cloud_ai_task_entity: CloudAITaskEntity,
    mock_handle_chat_log: AsyncMock,
) -> None:
    """Test generating plain text data."""
    chat_log = conversation.ChatLog(hass, "conversation-id")
    chat_log.async_add_user_content(
        conversation.UserContent(content="Tell me something")
    )
    task = ai_task.GenDataTask(name="Task", instructions="Say hi")

    async def fake_handle(chat_type, log, task_name, structure):
        """Inject assistant output."""
        assert chat_type == "ai_task"
        log.async_add_assistant_content_without_tools(
            conversation.AssistantContent(
                agent_id=mock_cloud_ai_task_entity.entity_id or "",
                content="Hello from the cloud",
            )
        )

    mock_handle_chat_log.side_effect = fake_handle
    result = await mock_cloud_ai_task_entity._async_generate_data(task, chat_log)

    assert result.conversation_id == "conversation-id"
    assert result.data == "Hello from the cloud"


async def test_generate_data_returns_json(
    hass: __HAC_KEEP__,
    mock_cloud_ai_task_entity: CloudAITaskEntity,
    mock_handle_chat_log: AsyncMock,
) -> None:
    """Test generating structured data."""
    chat_log = conversation.ChatLog(hass, "conversation-id")
    chat_log.async_add_user_content(conversation.UserContent(content="List names"))
    task = ai_task.GenDataTask(
        name="Task",
        instructions="Return JSON",
        structure=probatio.Schema({probatio.Required("names"): [str]}),
    )

    async def fake_handle(chat_type, log, task_name, structure):
        log.async_add_assistant_content_without_tools(
            conversation.AssistantContent(
                agent_id=mock_cloud_ai_task_entity.entity_id or "",
                content='{"names": ["A", "B"]}',
            )
        )

    mock_handle_chat_log.side_effect = fake_handle
    result = await mock_cloud_ai_task_entity._async_generate_data(task, chat_log)

    assert result.data == {"names": ["A", "B"]}


async def test_generate_data_invalid_json(
    hass: __HAC_KEEP__,
    mock_cloud_ai_task_entity: CloudAITaskEntity,
    mock_handle_chat_log: AsyncMock,
) -> None:
    """Test invalid JSON responses raise an error."""
    chat_log = conversation.ChatLog(hass, "conversation-id")
    chat_log.async_add_user_content(conversation.UserContent(content="List names"))
    task = ai_task.GenDataTask(
        name="Task",
        instructions="Return JSON",
        structure=probatio.Schema({probatio.Required("names"): [str]}),
    )

    async def fake_handle(chat_type, log, task_name, structure):
        log.async_add_assistant_content_without_tools(
            conversation.AssistantContent(
                agent_id=mock_cloud_ai_task_entity.entity_id or "",
                content="not-json",
            )
        )

    mock_handle_chat_log.side_effect = fake_handle
    with pytest.raises(
        __HAC_KEEP__Error, match="Error with OpenAI structured response"
    ):
        await mock_cloud_ai_task_entity._async_generate_data(task, chat_log)


async def test_generate_image_no_attachments(
    hass: __HAC_KEEP__, mock_cloud_ai_task_entity: CloudAITaskEntity
) -> None:
    """Test generating an image without attachments."""
    mock_cloud_ai_task_entity._cloud.llm.async_generate_image.return_value = {
        "mime_type": "image/png",
        "image_data": b"IMG",
        "model": "mock-image",
        "width": 1024,
        "height": 768,
        "revised_prompt": "Improved prompt",
    }
    task = ai_task.GenImageTask(name="Task", instructions="Draw something")
    chat_log = conversation.ChatLog(hass, "conversation-id")

    result = await mock_cloud_ai_task_entity._async_generate_image(task, chat_log)

    assert result.image_data == b"IMG"
    assert result.mime_type == "image/png"
    mock_cloud_ai_task_entity._cloud.llm.async_generate_image.assert_awaited_once_with(
        prompt="Draw something"
    )


async def test_generate_image_with_attachments(
    hass: __HAC_KEEP__,
    mock_cloud_ai_task_entity: CloudAITaskEntity,
    mock_prepare_generation_attachments: AsyncMock,
) -> None:
    """Test generating an edited image when attachments are provided."""
    mock_cloud_ai_task_entity._cloud.llm.async_edit_image.return_value = {
        "mime_type": "image/png",
        "image_data": b"IMG",
    }
    task = ai_task.GenImageTask(
        name="Task",
        instructions="Edit this",
        attachments=[
            conversation.Attachment(
                media_content_id="media-source://media/snapshot.png",
                mime_type="image/png",
                path=hass.config.path("snapshot.png"),
            )
        ],
    )
    chat_log = conversation.ChatLog(hass, "conversation-id")
    prepared_attachments = [
        LLMImageAttachment(filename="snapshot.png", mime_type="image/png", data=b"IMG")
    ]

    mock_prepare_generation_attachments.return_value = prepared_attachments
    await mock_cloud_ai_task_entity._async_generate_image(task, chat_log)

    mock_cloud_ai_task_entity._cloud.llm.async_edit_image.assert_awaited_once_with(
        prompt="Edit this",
        attachments=prepared_attachments,
    )


@pytest.mark.parametrize(
    ("err", "expected_exception", "message"),
    [
        (
            LLMAuthenticationError("auth"),
            __HAC_KEEP__Error,
            "Cloud LLM authentication failed",
        ),
        (
            LLMRateLimitError("limit"),
            __HAC_KEEP__Error,
            "Cloud LLM is rate limited",
        ),
        (
            LLMResponseError("bad response"),
            __HAC_KEEP__Error,
            "bad response",
        ),
        (
            LLMServiceError("service"),
            __HAC_KEEP__Error,
            "Error talking to Cloud LLM",
        ),
        (
            LLMError("generic"),
            __HAC_KEEP__Error,
            "generic",
        ),
    ],
)
async def test_generate_image_error_handling(
    hass: __HAC_KEEP__,
    mock_cloud_ai_task_entity: CloudAITaskEntity,
    err: Exception,
    expected_exception: type[Exception],
    message: str,
) -> None:
    """Test image generation error handling."""
    mock_cloud_ai_task_entity._cloud.llm.async_generate_image.side_effect = err
    task = ai_task.GenImageTask(name="Task", instructions="Draw something")
    chat_log = conversation.ChatLog(hass, "conversation-id")

    with pytest.raises(expected_exception, match=message):
        await mock_cloud_ai_task_entity._async_generate_image(task, chat_log)
