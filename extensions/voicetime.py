from nextcord import SlashOption
import nextcord, time, einstellungen, datetime, sqlite3
from nextcord.ext import commands
from main import Embed as Embed


class VoiceTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

    @commands.Cog.listener("on_voice_state_update")
    async def join(self, user, before, after):
        if before.channel is None and after.channel is not None:
            # user joined a voice channel
            self.joined = time.time()

        if before.channel is not None and after.channel is None:
            # user left a voice channel
            left = time.time()

            voicetime = left - self.joined
            # in minutes
            voicetime = round(voicetime / 60)

            self.bot.dbcursor.execute(
                f"INSERT INTO levels (id, voicetime) VALUES ({user.id}, {voicetime})"
            )
            self.bot.dbconn.commit()


def setup(bot):
    bot.add_cog(VoiceTime(bot))
