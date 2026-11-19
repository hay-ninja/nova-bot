"""Spotted features: tasks 1, 2 and 4 all live in this file.

Three people edit this file at once. To keep merges clean:
  - only edit inside your own TASK block,
  - the imports you need are already here.

Remember the rule: the bot gathers facts from Discord and shows the API's answer.
It does not decide what counts as a spot, how points work, or who's ranked where.
"""

from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from bot import config
from bot.api_client import api


class Spotted(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # =================================================================
    # TASK 1: #spotted listener -> POST /spots
    # =================================================================
    # discord.py calls this for EVERY message the bot can see.
    #   - ignore messages from bots, and messages outside SPOTTED_CHANNEL_ID
    #   - send the raw facts to POST /spots (see SpotIn in api/models.py):
    #       spotter_id       = str(message.author.id)
    #       spotted_ids      = [str(user.id) for user in message.mentions]
    #       attachment_types = [a.content_type or "" for a in message.attachments]
    #       message_id, channel_id as strings
    #   - 201 -> react with 📸
    #     409 -> do nothing (already counted)
    #     400 -> reply with resp.json()["detail"]
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        pass




    # =================================================================
    # TASK 2: /mystats [user] -> GET /users/{id}/stats
    # =================================================================
    #   - if `user` is None, use the person who ran the command (interaction.user)
    #   - show spots given, spots received, rank, and who they spot most
    #   - tip: f"<@{some_id}>" shows as a name in Discord
    @app_commands.command(name="mystats", description="Show spots given and received")
    @app_commands.describe(user="Whose stats to show (default: you)")
    async def mystats(self, interaction: discord.Interaction, user: discord.Member | None = None) -> None:
        await interaction.response.send_message("🚧 /mystats isn't built yet (task 2)", ephemeral=True)




    # =================================================================
    # TASK 4: /leaderboard [period] -> GET /leaderboard
    # =================================================================
    #   - call the API with limit=10 and the chosen period
    #   - show the result as a discord.Embed, one line per entry: "1. <@id> - 7 pts"
    #     (mentions inside embeds show names and never ping anyone)
    #   - handle an empty leaderboard nicely
    @app_commands.command(name="leaderboard", description="Top spotters")
    @app_commands.describe(period="All time or the last 7 days")
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        period: Literal["all", "week"] = "all",
    ) -> None:
        await interaction.response.send_message("🚧 /leaderboard isn't built yet (task 4)", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Spotted(bot))
