"""Daily birthday post (task 5)."""

import logging
from datetime import time
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from bot import config
from bot.api_client import api

log = logging.getLogger("bot.birthdays")

LA = ZoneInfo("America/Los_Angeles")
POST_AT = time(hour=0, minute=0, tzinfo=LA)  # midnight in LA, whatever the server's clock says


class Birthdays(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        self.daily_post.start()

    async def cog_unload(self) -> None:
        self.daily_post.cancel()

    # =================================================================
    # TASK 5: daily birthday post -> GET /members/birthdays/today
    # =================================================================
    # discord.py runs this once a day at POST_AT.
    #   - ask the API who has a birthday today
    #   - nobody -> post nothing
    #   - otherwise post ONE message in BIRTHDAY_CHANNEL_ID mentioning everyone:
    #       "🎂 Happy birthday <@id1> and <@id2>!"
    #     (here mentions DO ping, which is the point)
    #   - testing tip: temporarily change POST_AT to a minute from now,
    #     or call the endpoint with ?date= in /docs
    @tasks.loop(time=POST_AT)
    async def daily_post(self) -> None:
        log.info("Birthday job ran, but task 5 isn't built yet")

    @daily_post.before_loop
    async def before_daily_post(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Birthdays(bot))
