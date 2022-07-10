from codecs import Codec
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


class Abstimmung:
    def __init__(self, language, codefile):
        self.language = language
        self.codefile = codefile

    class AbstimmButtons(nextcord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @nextcord.ui.button(label="Ja", style=nextcord.ButtonStyle.primary)
        async def yes(self, button: nextcord.Button,
                      interaction: nextcord.Interaction):

            communitycode = interaction.guild.get_channel(994933082425663498)
            communityembed = Embed(
                title=f"Neues {Abstimmung.language}-Code-Snippet",
                description=f"{interaction.user.mention} hat ein Code-Snippet hochgeladen.",
                color=nextcord.Colour.green(),
            )
            await communitycode.send(content="<@&995670130019283035>", embed=communityembed)
            await communitycode.send(file=Abstimmung.codefile)


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

        await code.save("snippets/community/" + code.filename)
        # Edit the file and write from who the file was sent
        with open("snippets/community/" + code.filename, "r") as f:
            lines = f.readlines()
        with open("snippets/community/" + code.filename, "w") as f:
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
        codefile = nextcord.File("snippets/community/" + code.filename)
        await teamchannel.send(embed=teamembed, content="<@&994857229280882709>")
        await teamchannel.send(file=codefile)

        # communitycode = interaction.guild.get_channel(994933082425663498)
        # communityembed = Embed(
        #     title=f"Neues {language}-Code-Snippet",
        #     description=f"{interaction.user.mention} hat ein Code-Snippet hochgeladen.",
        #     color=nextcord.Colour.green(),
        # )
        # await communitycode.send(content="<@&995670130019283035>", embed=communityembed)
        # await communitycode.send(file=codefile)

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
