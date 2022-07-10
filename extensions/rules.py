import asyncio
from nextcord import SlashOption
import nextcord
import time
import settings
import datetime
import sqlite3
from nextcord.ext import commands
from main import Embed as Embed
from main import YesNoButtons as YesNoButtons


class RuleLinks(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(nextcord.ui.Button(label="Terms of Service",
                                         url="https://discord.com/terms"))

        self.add_item(nextcord.ui.Button(label="Guidelines",
                                         url="https://discord.com/guidelines"))

        self.add_item(nextcord.ui.Button(label="Privacy Policy",
                                         url="https://discord.com/privacy"))


class RulesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

    @ nextcord.slash_command(name="rules", description="[ 📛 Admin 📛 ] Sende die Regeln des Servers.", guild_ids=[settings.guild], default_member_permissions=8)
    async def rules(self,
                    interaction: nextcord.Interaction,
                    channel: nextcord.abc.GuildChannel = SlashOption(
                        required=False, description="[ 📛 Admin 📛 ] Sende die Regeln des Server in diesen Kanal.")
                    ):

        if channel is None:
            channel = interaction.channel

        embed = Embed(
            title="Regeln",
            description="""
            ```
1. Keine Beleidigungen
            
2. Keine Regelwerk-Grauzonen ausnutzen, sondern melden
            
3. Ohne Berechtigung von einem Mitglied der Mitarbeiter kein Spam oder Eigenwerbung (Server-Einladungen, Anzeigen, usw.). Dazu zählen auch Direktnachrichten an andere Mitglieder.
            
4. Discord ToS: u.a Mindestalter
            
5. Behandle alle mit Respekt. Belästigung, Hexenjagd, Sexismus, Rassismus oder Volksverhetzung werden absolut nicht toleriert.
            
6. Keine altersbegrenzten oder obszönen Inhalte. Dazu zählen Texte, Bilder oder Links mit Nacktheit, Sex, schwerer Gewalt oder anderen grafisch verstörenden Inhalten.
            
7. Wenn du etwas sieht, das gegen die Regeln verstößt, oder wodurch du dich nicht sicher fühlst, dann benachrichtige die Mitarbeiter. Wir möchten, dass dieser Server ein Ort ist, an dem sich jeder willkommen fühlt.
```
            """,
            color=nextcord.Colour.green(),
        )

        await channel.send(embed=embed, view=RuleLinks())
        await interaction.response.send_message("Regeln wurden gesendet.", ephemeral=True)


def setup(bot):
    bot.add_cog(RulesCommand(bot))
