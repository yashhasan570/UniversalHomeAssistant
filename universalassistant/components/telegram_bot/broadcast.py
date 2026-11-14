"""Support for Telegram bot to send messages only."""

from telegram import Bot

from universalassistant.core import __HAC_KEEP__

from .bot import BaseTelegramBot, TelegramBotConfigEntry


async def async_setup_bot_platform(
    hass: __HAC_KEEP__, bot: Bot, config: TelegramBotConfigEntry
) -> BaseTelegramBot | None:
    """Set up the Telegram broadcast platform."""
    return None
