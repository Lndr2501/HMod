from codecs import Codec
import os
from pydoc import describe
from re import A
from nextcord import Interaction, SlashOption
import nextcord
import time
import settings
import datetime
import sqlite3
from nextcord.ext import commands
from main import Embed as Embed

supported_languages = [
    "Python",
    "JavaScript",
    "Java",
    "C",
    "C++",
    "C#",
    "Go",
]


class CodeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.extras = extras

    @ nextcord.slash_command(name="code", description="[ 👥 Mitglied 👥 ] Sende ein Code-Snippet ein.")
    async def code(self, interaction: nextcord.Interaction, code: nextcord.Attachment = SlashOption()):
        ...

    @ code.subcommand(name="community", description="[ 👥 Mitglied 👥 ] Sende ein Code-Snippet ein.")
    async def community(self, interaction: nextcord.Interaction, language: str = SlashOption(description="[ 👥 Mitglied 👥 ] Welche Programmiersprache?"), code: nextcord.Attachment = SlashOption()):
        if language not in supported_languages:
            embed = Embed(
                title="Fehler",
                description="Diese Sprache wird nicht unterstützt.",
                color=nextcord.Colour.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        ending = ""
        if language == "Python":
            ending = ".py"
        elif language == "JavaScript":
            ending = ".js"
        elif language == "Java":
            ending = ".java"
        elif language == "C":
            ending = ".c"
        elif language == "C++":
            ending = ".cpp"
        elif language == "C#":
            ending = ".cs"
        elif language == "Go":
            ending = ".go"

        if not code.filename.endswith(ending):
            wrongfileending = code.filename.split(".")[-1]

            embed = Embed(
                title="Fehler",
                description=f"Du hast eine Datei mit der Endung {wrongfileending} hochgeladen, aber du hast eine Sprache mit der Endung {ending} gewählt.",
                color=nextcord.Colour.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await code.save("snippets/community/" + interaction.user.name + "_" + code.filename)
        # Edit the file and write from who the file was sent
        with open("snippets/community/" + interaction.user.name + "_" + code.filename, "r") as f:
            lines = f.readlines()
        with open("snippets/community/" + interaction.user.name + "_" + code.filename, "w") as f:
            kommentar = ""
            if ending == ".py":
                kommentar = "#"
            elif ending == ".js":
                kommentar = "//"
            elif ending == ".java":
                kommentar = "//"
            elif ending == ".c":
                kommentar = "//"
            elif ending == ".cpp":
                kommentar = "//"
            elif ending == ".cs":
                kommentar = "//"
            elif ending == ".go":
                kommentar = "//"
            # Write who sent the file and the time it was sent at the end of the file
            lines.append(
                f"{kommentar} {interaction.user.name} ({interaction.user.id}) hat die Datei {code.filename} am {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')} hochgeladen.")
            f.writelines(lines)

        teamembed = Embed(
            title="Code-Snippet hochgeladen",
            description=f"{interaction.user.mention} ({interaction.user.id}) hat ein Code-Snippet hochgeladen.",
            color=nextcord.Colour.green(),
        )
        # Send the file
        teamchannel = interaction.guild.get_channel(995658446236029028)
        codefile = nextcord.File(
            "snippets/community/" + interaction.user.name + "_" + code.filename)
        await teamchannel.send(embed=teamembed, content="<@&994857229280882709>")

        class AbstimmButtons(nextcord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @nextcord.ui.button(label="Hochladen", style=nextcord.ButtonStyle.primary)
            async def yes(self, button: nextcord.Button,
                          interaction: nextcord.Interaction):

                communitycode = interaction.guild.get_channel(
                    994933082425663498)
                communityembed = Embed(
                    title=f"Neues {language}-Code-Snippet",
                    description=f"{interaction.user.mention} hat ein Code-Snippet hochgeladen.",
                    color=nextcord.Colour.green(),
                )
                codefile = nextcord.File(
                    "snippets/community/" + interaction.user.name + "_" + code.filename)
                await communitycode.send(content="<@&995670130019283035>", embed=communityembed)
                await communitycode.send(file=codefile)

                # Delete the file after it was sent
                os.remove("snippets/community/" +
                          interaction.user.name + "_" + code.filename)

                succesembed = Embed(
                    title="Code-Snippet hochgeladen",
                    description=f"Das Code-Snippet ist nun auf der Community-Seite verfügbar.",
                    color=nextcord.Colour.green(),
                )
                await interaction.response.send_message(embed=succesembed, ephemeral=True)

                button.disabled = True
                button.label = "Hochgeladen"

                self.no.disabled = True
                self.no.label = f"~~{self.no.label}~~"

                await tmsg.edit(file=codefile, view=self)

            @nextcord.ui.button(label="Löschen", style=nextcord.ButtonStyle.danger)
            async def no(self, button: nextcord.Button,
                         interaction: nextcord.Interaction):

                # Delete the file after it was sent
                os.remove("snippets/community/" +
                          interaction.user.name + "_" + code.filename)

                succesembed = Embed(
                    title="Code-Snippet nicht hochgeladen",
                    description=f"Das Code-Snippet ist abgelehnt worden, und wurde gelöscht.",
                    color=nextcord.Colour.red(),
                )
                await interaction.response.send_message(embed=succesembed, ephemeral=True)

                button.disabled = True
                button.label = "Abgelehnt"

                self.yes.disabled = True
                self.yes.label = f"~~{self.yes.label}~~"

                await tmsg.edit(file=codefile, view=self)

        tmsg = await teamchannel.send(file=codefile, view=AbstimmButtons())

        embed = Embed(
            title="Erfolgreich",
            description="Dein Code-Snippet wurde erfolgreich hochgeladen. Der Code wird nun von unseren Entwicklern überprüft und danach in den Community-Kanal gepostet.",
            color=nextcord.Colour.green(),
        )
        await interaction.response.send_message(embed=embed)

    @ community.on_autocomplete("language")
    async def langauto(self, interaction: Interaction, language: str):
        if not language:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(supported_languages)
            return
        # send a list of nearest matches from the list of dog breeds
        get_near_lang = [
            breed for breed in supported_languages if breed.lower().startswith(language.lower())
        ]
        await interaction.response.send_autocomplete(get_near_lang)


def setup(bot):
    bot.add_cog(CodeCommand(bot))
