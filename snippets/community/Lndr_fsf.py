import nextcord
from nextcord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot, extras: dict = None):
        self.bot = bot
        self.extras = extras

    @commands.Cog.listener("on_ready")
    async def onready(self):
        print(f"Der Bot {self.bot.user.name} ist bereit.")


def setup(bot, extras: dict = None):
    bot.add_cog(Events(bot, extras))# Lndr (927148345263271937) hat die Datei fsf.py am 10.07.2022 20:59:02 hochgeladen.