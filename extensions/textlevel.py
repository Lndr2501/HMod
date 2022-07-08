from datetime import datetime
from nextcord import SlashOption
import einstellungen, nextcord, random
from nextcord.ext import commands
from main import Embed


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

        self.leveloptionen = [
            "Text Level",
            "Voice Level",
        ]

    @commands.Cog.listener("on_message")
    async def textlevel(self, message: nextcord.Message):
        xp = len(message.content) / 2
        data = self.bot.dbcursor.execute(
            'SELECT "text_xp" FROM levels WHERE "id" = ?', (message.author.id,)
        ).fetchone()

        if not data:
            xp_before = 0
            self.bot.dbcursor.execute(
                'INSERT INTO levels ("text_xp", "id") VALUES (?, ?)',
                (xp, message.author.id),
            )
            xp_after = xp

        else:
            xp_before = data[0]
            self.bot.dbcursor.execute(
                'UPDATE levels SET "text_xp" = ? WHERE "id" = ?',
                (data[0] + xp, message.author.id),
            )
            xp_after = data[0] + xp

        if self.bot.calculate_level(xp_before) < self.bot.calculate_level(xp_after):
            embed = Embed(
                title=f"Levelup",
                description=f"Toll {message.author.mention}! Du hast Level {self.bot.calculate_level(xp_after)} erreicht!",
            )
            await message.channel.send(
                embed=embed, content=f"{message.author.mention}", delete_after=15
            )

        self.bot.dbconn.commit()


def setup(bot):
    bot.add_cog(LevelSystem(bot))
