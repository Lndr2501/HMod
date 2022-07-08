from matplotlib.pyplot import title
from matplotlib.style import use
from nextcord import SlashOption
import nextcord, time, einstellungen, datetime, sqlite3
from nextcord.ext import commands
from main import Archivment, ArchivmentType, Embed as Embed


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

            if voicetime is None:
                embed = Archivment(archivment=ArchivmentType.FIRST_VOICE)
                await user.send(embed=embed)

            # when voicetime over 10 minuten, level up
            if voicetime > 600:
                self.bot.dbcursor.execute(f"UPDATE levels SET level = level + 1 WHERE id = {user.id}")
                self.bot.dbcursor.execute(f"UPDATE levels SET voicetime = 0 WHERE id = {user.id}")
                
                voicelevel = self.bot.dbcursor.execute(f"SELECT voicelevel FROM levels WHERE id = {user.id}").fetchone()[0]
                embed = Embed(
                    title=f"Sprachlevel erhöht",
                    description=f"{user.mention} hat sein Sprachlevel erhöht auf {voicetime}",
                    color=nextcord.Color.green(),
                )
                await user.send(embed=embed)

            



            
    

def setup(bot):
    bot.add_cog(VoiceLevel(bot))
