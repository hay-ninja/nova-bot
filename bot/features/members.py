"""Member lookup (task 3)."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.api_client import api


class Members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # =================================================================
    # TASK 3: /member name:<text>  or  /member user:@someone
    # =================================================================
    #   - exactly one of `name` or `user` should be given; otherwise reply asking for one
    #   - name -> GET /members?name=...      (a list: 0, 1 or several matches)
    #     user -> GET /members/{user.id}     (one member, or 404)
    #   - user -> 404 can also mean "their Discord ID isn't in the roster yet"; suggest searching by name
    #   - show each member as a discord.Embed (name, pronouns, major, class year,
    #     involvement, skills, GitHub, email, phone); skip empty fields
    #     (github is a username: link it as https://github.com/<username>)
    #   - always reply with ephemeral=True so personal info stays out of the channel
    #   - several matches: show up to 5 embeds (send_message(embeds=[...]))
    @app_commands.command(name="member", description="Look up a club member")
    @app_commands.describe(name="Part of their name", user="Or pick them directly")
    async def member(
        self,
        interaction: discord.Interaction,
        name: str | None = None,
        user: discord.Member | None = None,
    ) -> None:
        await interaction.response.send_message("🚧 /member isn't built yet (task 3)", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Members(bot))
