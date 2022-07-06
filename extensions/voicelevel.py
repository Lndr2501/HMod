from matplotlib.pyplot import title
from nextcord import SlashOption
import nextcord, time, einstellungen, datetime, sqlite3
from nextcord.ext import commands
from main import Embed as Embed


class VoiceLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.extras = extras

    @commands.Cog.listener("on_voice_state_update")
    async def join(self, user, before, after):
        if before.channel is None and after.channel is not None:
            # user joined a voice channel
            # if voicetime 10 minuten oder mehr, dann level up
            voicetime = self.bot.dbcursor.execute(f"SELECT voicetime FROM levels WHERE id = {user.id}").fetchone()[0]

            # convert voicetime to int with round() and convert to minutes
            print(voicetime(type))

            if voicetime >= 10:
                # level up
                self.bot.dbcursor.execute(f"UPDATE levels SET voicelevel = voicelevel + 1 WHERE id = {user.id}")
                self.bot.dbconn.commit()

                # reset voicetime
                self.bot.dbcursor.execute(f"UPDATE levels SET voicetime = 0 WHERE id = {user.id}")
                self.bot.dbconn.commit()


                # send message
                newlevel = self.bot.dbcursor.execute(f"SELECT voicelevel FROM levels WHERE id = {user.id}").fetchone()[0]
                embed = Embed(
                    title=f"Sprachlevel erhöht",
                    description=f"{user.mention} hat sein Sprachlevel erhöht auf {newlevel}",
                    color=nextcord.Color.green(),
                )
                await after.channel.send(embed=embed, content=f"{user.mention}")




            
    

def setup(bot):
    bot.add_cog(VoiceLevel(bot))
