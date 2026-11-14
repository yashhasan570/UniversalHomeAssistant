"""AI Task integration for Anthropic."""

from json import JSONDecodeError
import logging
from typing import TYPE_CHECKING, override

from universalassistant.components import ai_task, conversation
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.util.json import json_loads

from .const import DOMAIN
from .entity import AnthropicBaseLLMEntity

if TYPE_CHECKING:
    from .coordinator import AnthropicConfigEntry

PARALLEL_UPDATES = 0

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: AnthropicConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AI Task entities."""
    for subentry in config_entry.subentries.values():
        if subentry.subentry_type != "ai_task_data":
            continue

        async_add_entities(
            [AnthropicTaskEntity(config_entry, subentry)],
            config_subentry_id=subentry.subentry_id,
        )


class AnthropicTaskEntity(
    ai_task.AITaskEntity,
    AnthropicBaseLLMEntity,
):
    """Anthropic AI Task entity."""

    _attr_supported_features = (
        ai_task.AITaskEntityFeature.GENERATE_DATA
        | ai_task.AITaskEntityFeature.SUPPORT_ATTACHMENTS
    )
    _attr_translation_key = "ai_task_data"

    @override
    async def _async_generate_data(
        self,
        task: ai_task.GenDataTask,
        chat_log: conversation.ChatLog,
    ) -> ai_task.GenDataTaskResult:
        """Handle a generate data task."""
        await self._async_handle_chat_log(chat_log, task.structure, max_iterations=1000)

        if not isinstance(chat_log.content[-1], conversation.AssistantContent):
            raise UniversalAssistantError(
                translation_domain=DOMAIN, translation_key="response_not_found"
            )

        text = chat_log.content[-1].content or ""

        if not task.structure:
            return ai_task.GenDataTaskResult(
                conversation_id=chat_log.conversation_id,
                data=text,
            )
        try:
            data = json_loads(text)
        except JSONDecodeError as err:
            # pylint: disable-next=universal-assistant-log-and-raise
            _LOGGER.error(
                "Failed to parse JSON response: %s. Response: %s",
                err,
                text,
            )
            raise UniversalAssistantError(
                translation_domain=DOMAIN, translation_key="json_parse_error"
            ) from err

        return ai_task.GenDataTaskResult(
            conversation_id=chat_log.conversation_id,
            data=data,
        )
