"""Support for Telegram bot to send messages only."""

from telegram import Bot

from universalassistant.core import UniversalAssistant

from .bot import BaseTelegramBot, TelegramBotConfigEntry


async def async_setup_bot_platform(
    hass: UniversalAssistant, bot: Bot, config: TelegramBotConfigEntry
) -> BaseTelegramBot | None:
    """Set up the Telegram broadcast platform."""
    return None
