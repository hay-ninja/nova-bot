"""The bot program. Run it with:  python -m bot.main

It logs in to Discord with your token, loads each feature file in bot/features/,
and registers the slash commands to your server (GUILD_ID) so they show up instantly.
"""

import logging

import discord
import httpx
from discord import app_commands
from discord.ext import commands

from bot import config
from bot.api_client import api

log = logging.getLogger("bot")

# Each entry is a file in bot/features/. Each file defines one "Cog":
# discord.py's name for a class that groups related commands and listeners.
FEATURES = [
    "bot.features.health",
    "bot.features.spotted",
    "bot.features.members",
    "bot.features.birthdays",
]


class SpottedBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  # needed to read #spotted posts; also enable it in the Developer Portal
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def setup_hook(self) -> None:
        for feature in FEATURES:
            await self.load_extension(feature)

        # Register slash commands to our one server only, so changes appear instantly.
        guild = discord.Object(id=config.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)
        log.info("Synced %d slash commands to guild %s", len(synced), config.GUILD_ID)

        self.tree.error(on_command_error)

    async def on_ready(self) -> None:
        log.info("Logged in as %s (id %s)", self.user, self.user.id)

    async def close(self) -> None:
        await api.close()
        await super().close()


async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    """Runs when any slash command crashes, so users see a message instead of 'The application did not respond'."""
    original = getattr(error, "original", error)
    if isinstance(original, httpx.HTTPError):
        message = "I can't reach the API right now. Is it running?"
    else:
        message = "Something went wrong. Check the bot's logs."
    log.error("Error in /%s", interaction.command.name if interaction.command else "?", exc_info=original)

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


def main() -> None:
    discord.utils.setup_logging(level=logging.INFO)
    SpottedBot().run(config.DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
