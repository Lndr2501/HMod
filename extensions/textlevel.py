from datetime import datetime
from nextcord import SlashOption
import settings, nextcord, random
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

    # FIXME
    # @commands.Cog.listener("on_message")
    # async def textlevel(self, message: nextcord.Message):
    #     if message.author.bot:
    #         return


    #     xp = random.randint(5, 10)
    #     await message.reply("Xp Generiert: " + str(xp))

    #     data = self.bot.dbcursor.execute("SELECT 'text_xp' FROM levels WHERE id = ?", (message.author.id,)).fetchone()
    #     await message.reply("Datenbank abgefragt")

    #     if not data:
    #         await message.reply("Datenbank leer")
    #         xp_before = 0
    #         self.bot.dbcursor.execute("INSERT INTO levels ('text_xp', 'id') VALUES (?, ?)", (xp, message.author.id))
    #         xp_after = xp
    #     else:
    #         await message.reply("Datenbank nicht leer")
    #         xp_before = data[0]
    #         self.bot.dbcursor.execute("UPDATE levels SET 'text_xp' = ? WHERE id = ?", (data[0] + xp, message.author.id))
    #         xp_after = data[0] + xp

    #     self.bot.dbconn.commit()
    #     await message.reply(" Datenbank gespeichert")

        

            
def setup(bot):
    bot.add_cog(LevelSystem(bot))
