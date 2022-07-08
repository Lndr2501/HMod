import sqlite3
from traceback import format_exception
import aiosqlite
import nextcord, os, io, contextlib, textwrap, main, aiohttp
from nextcord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

    @commands.Cog.listener("on_ready")
    async def on_ready(self):

        print(f"Eingeloggt als {self.bot.user.name}. ID: {self.bot.user.id}")

        await self.bot.change_presence(activity=nextcord.Game(name=self.bot.game))
        print(f"Status: Online. Spiel: {self.bot.game}")


def setup(bot):
    bot.add_cog(OnReady(bot))
