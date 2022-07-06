from traceback import format_exception
import nextcord, os, io, contextlib, textwrap
from main import Embed as Embed
from nextcord.ext import commands

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.extras = extras

    @commands.command(name="eval", aliases=["run"])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, code):

        code = code.strip("`") # Remove code block
        code = code.strip("py")

        
        local_variables = {
            "nextcord": nextcord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
                color = nextcord.Color.green()

        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            color = nextcord.Color.red()


        embed = Embed(
        title="Eval Ergebnis",
        description="```py\n" + result + "```",
        color=color,
        )
        await ctx.send(content=f"{ctx.author.mention}", cembed=embed)


def setup(bot):
    bot.add_cog(Eval(bot))