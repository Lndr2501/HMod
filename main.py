from enum import Enum
import os, nextcord, einstellungen, datetime, sqlite3

from matplotlib import image
from numpy import imag
from click import command
from nextcord import Colour
from nextcord.ext import commands
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

intents = nextcord.Intents.default()
intents.members = True


# Klass für die Erstellung von Bannern
class Banner:
    def __init__(self, text, color):
        self.text = text
        self.color = color

    def create(self):
        background = Image.open("./images/Banner.png")
        draw = ImageDraw.Draw(background)
        # get perfect font size
        font = ImageFont.truetype("./arial.ttf", size=int(background.size[1] / 2))
        # get text size
        text_size = draw.textsize(self.text, font=font)
        # get the middle of the image
        w, h = background.size
        text_width, text_height = draw.textsize(self.text, font=font)
        text_x = (w - text_width) / 2
        text_y = (h - text_height) / 2
        draw.text((text_x, text_y), self.text, font=font, fill=self.color)

        text = self.text.replace("#", "")
        text = text.replace(" ", "_")

        background.save(f"./images/Banner_{text}.png")
        return f"./images/Banner_{text}.png"


class Embed(nextcord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_image(url="https://i.imgur.com/9Fka6pN.png")
        self.set_footer(text=" ", icon_url="https://imgur.com/a/cAZMGH1.jpeg")
        self.timestamp = datetime.datetime.now()


class ArchivmentType(Enum):
    FIRST_VOICE = [
        "Erstes mal in einem Sprachkanal!",
        "Du bist zum ersten mal in einem Sprachkanal! :D",
    ]
    FIRST_MESSAGE = [
        "Erstes mal Geschrieben!",
        "Du hast zum ersten mal etwas in den Chat geschrieben! :D",
    ]


class Archivment:
    def __init__(self, user: nextcord.Member, type: ArchivmentType):
        self.user = user
        self.type = type
        self.date = datetime.datetime.now()

        embed = Embed(
            title=type.value[0],
            description=type.value[1],
            color=nextcord.Colour.green(),
            timestamp=self.date,
        )
        embed.set_image(url="https://cdn.discordapp.com/emojis/938532159554220112.gif")

        return embed


class Bot(commands.Bot):
    def __init__(
        self, command_prefix=..., help_command=..., intents=..., owner_id=..., **options
    ):
        super().__init__(
            command_prefix=command_prefix,
            help_command=help_command,
            intents=intents,
            owner_id=owner_id,
            **options,
        )

        self.dbconn: sqlite3.Connection = sqlite3.connect("./database.db")
        self.dbcursor: sqlite3.Cursor = self.dbconn.cursor()

        self.token = einstellungen.token
        self.game = einstellungen.game
        self.server = einstellungen.guild

        @self.command()
        @commands.is_owner()
        async def reload(ctx: commands.Context):
            reloaded = []
            for file in os.listdir("./extensions"):
                if file.endswith(".py"):
                    name = file[:-3]

                    self.reload_extension(f"extensions.{name}")
                    reloaded.append(name)
                else:
                    print(f"Skipping {file}")

            await ctx.send(f"Reloaded: {', '.join(reloaded)}")

        for file in os.listdir("./extensions"):
            if file.endswith(".py"):
                name = file[:-3]

                self.load_extension(f"extensions.{name}")
                print(f"Loaded {name}")
            else:
                print(f"Skipping {file}")


# Create a bot instance and run it.
bot = Bot(
    command_prefix=commands.when_mentioned,
    owner_id=einstellungen.owner,
    help_command=None,
    intents=intents,
)
bot.run(bot.token)
