from tkinter import N
from nextcord import SlashOption
import nextcord
import time
import settings
import datetime
import sqlite3
from nextcord.ext import commands
from main import Embed as Embed


class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.extras = extras

    @nextcord.slash_command(name="clear", description="[ 📛 Manage messages 📛 ] Leere den Chat.", default_member_permissions=131072)
    async def clear(self,
                    interaction: nextcord.Interaction,
                    amount: int = SlashOption(
                        description="[ 📛 Manage messages 📛 ] Wie viele Nachrichten löschen?", required=False, default=10),
                    channel: nextcord.abc.GuildChannel = SlashOption(
                        description="[ 📛 Manage messages 📛 ] In welchem Kanal?", required=False)
                    ):
        if channel is None:
            channel = interaction.channel

        # delete messages and show how many messages were deleted
        await channel.purge(limit=amount)

        embed = Embed(
            title="Erfolgreich",
            description=f"{amount} Nachrichten wurden gelöscht.",
            color=nextcord.Colour.green(),
            timestamp=datetime.datetime.now(),
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(ClearCommand(bot))
