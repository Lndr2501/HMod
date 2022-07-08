from nextcord import SlashOption
import datetime
import nextcord
from nextcord.ext import commands
from main import Embed as Embed


class VoiceTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

        self.in_voice: dict[int, datetime.datetime] = {}

    @commands.Cog.listener("on_voice_state_update")
    async def voicetime(
        self,
        member: nextcord.Member,
        before: nextcord.VoiceState,
        after: nextcord.VoiceState,
    ):
        if not before.channel and after.channel:
            self.in_voice.update({member.id: datetime.datetime.now()})

        elif before.channel and not after.channel:
            if time := self.in_voice.get(member.id):
                minutes = int((datetime.datetime.now() - time).total_seconds() / 60)
                if not minutes > 0:
                    return
                xp = minutes * 10
                data = self.bot.dbcursor.execute(
                    'SELECT "voice_xp" FROM levels WHERE "id" = ?', (member.id,)
                ).fetchone()
                if not data:
                    xp_before = 0
                    self.bot.dbcursor.execute(
                        'INSERT INTO levels ("voice_xp", "id") VALUES (?, ?)',
                        (xp, member.id),
                    )
                    xp_after = xp
                else:
                    xp_before = data[0]
                    self.bot.dbcursor.execute(
                        'UPDATE levels SET "voice_xp" = ? WHERE "id" = ?',
                        (data[0] + xp, member.id),
                    )
                    xp_after = data[0] + xp
                self.bot.dbconn.commit()

                if (lvl_before := self.bot.calculate_level(xp_before)) < (
                    lvl_after := self.bot.calculate_level(xp_after)
                ):
                    embed = Embed(
                        title=f"Levelup",
                        description=f"Toll {member.mention}! Du hast Level {lvl_after} erreicht!",
                    )
                    await member.send(embed=embed)


def setup(bot):
    bot.add_cog(VoiceTime(bot))
