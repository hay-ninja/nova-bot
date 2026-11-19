"""Worked example: /ping. Read this before starting your task.

It shows the whole round trip every feature follows:
  1. Discord tells the bot someone ran /ping        (discord.py calls ping())
  2. the bot asks the API                            (api.get("/health"))
  3. the API answers with JSON                       (api/main.py, health())
  4. the bot turns the answer into a Discord message (send_message)
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.api_client import api


class Health(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check that the bot can reach the API")
    async def ping(self, interaction: discord.Interaction) -> None:
        resp = await api.get("/health")
        data = resp.json()  # {"status": "ok", "spots": 12, "members": 8}
        await interaction.response.send_message(
            f"🏓 API is up: {data['spots']} spots and {data['members']} members in the database.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Health(bot))
