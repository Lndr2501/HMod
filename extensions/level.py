from datetime import datetime
from nextcord import SlashOption
import einstellungen, nextcord, random
from nextcord.ext import commands
from main import Embed

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.extras = extras

        self.leveloptionen = [
            "Text Level",
            "Voice Level",
        ]


    @commands.Cog.listener("on_message")
    async def farmxp(self, message: nextcord.Message):
        if message.author.bot:
            return
        xp = random.randint(3, 10)
        oldxp = self.bot.dbcursor.execute(f"SELECT textxp FROM levels WHERE id = {message.author.id}").fetchone()[0]

        self.bot.dbcursor.execute(f"UPDATE levels SET textxp = {oldxp + xp} WHERE id = {message.author.id}")
        self.bot.dbconn.commit()

        await self.checkxp(message.author.id, message.channel)
    

    async def checkxp(self, userid, channel: nextcord.TextChannel):
        xp = self.bot.dbcursor.execute(f"SELECT textxp FROM levels WHERE id = {userid}").fetchone()[0]
        level = self.bot.dbcursor.execute(f"SELECT textlevel FROM levels WHERE id = {userid}").fetchone()[0]
        if xp >= 100:
            self.bot.dbcursor.execute(f"UPDATE levels SET textxp = 0, level = {level + 1} WHERE id = {userid}")
            self.bot.dbconn.commit()

            user = self.bot.get_user(userid)

            embed = Embed(
                title="Level up!",
                description=f"Mach weiter so! Du bist nun Level {level + 1}!",
                color=nextcord.Colour.green(),
            )
            await channel.send(content=f"{user.mention}", embed=embed)

            return True
        else:
            return False
    

    @nextcord.slash_command(name="level", description="[ @everyone ] Zeigt dein Level an, oder eines anderen Nutzers an.", guild_ids=[993355470087651368])
    async def level(self, interaction: nextcord.Interaction,
     #option = SlashOption(description="[ @everyone ] Welches Level anzeigen?", required=True),
     user: nextcord.Member = SlashOption(description="[ @everyone ] Zeigt das Level eines anderen Nutzers an.", required=False)):
        if user == None:
            user = interaction.user
        
        if user.bot:
            embed = nextcord.Embed(
                title="Fehler",
                description="Bots können kein Level haben!",
                color=nextcord.Colour.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        xp = self.bot.dbcursor.execute(f"SELECT textxp FROM levels WHERE id = {user.id}").fetchone()[0]
        level = self.bot.dbcursor.execute(f"SELECT level FROM levels WHERE id = {user.id}").fetchone()[0]
        embed = Embed(
            title=f"Level von {user.display_name}",
            description=f"Mach weiter so! Du bist Level {level} mit {xp} XP.",
            color=nextcord.Colour.green(),
        )
        await interaction.response.send_message(content=f"{user.mention}", embed=embed)


def setup(bot):
    bot.add_cog(LevelSystem(bot))