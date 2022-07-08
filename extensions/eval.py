import datetime
from traceback import format_exception
from unittest import result
import nextcord, os, io, contextlib, textwrap
from main import Embed as Embed
from nextcord.ext import commands
import aioconsole
import asyncio
import io
import sys


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        # a command to run code in the bot's environment (for debugging purposes)

        # FIXME
        try:
            variables = {
                "ctx": ctx,
                "bot": self.bot,
                "nextcord": nextcord,
                "__import__": __import__,
            }
            out = io.StringIO()
            sys.stdout = out
            await aioconsole.aexec(code, variables)
            sys.stdout = sys.__stdout__
            result = out.getvalue()

        except Exception as e:
            embed = Embed(
                title="Eval - Error",
                description=f"```py\n{format_exception(type(e), e, e.__traceback__)}```",
                color=nextcord.Colour.red(),
                timestamp=datetime.datetime.now(),
            )
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Eval(bot))
