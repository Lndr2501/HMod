import sqlite3
from traceback import format_exception
import aiosqlite
import nextcord, os, io, contextlib, textwrap, main, aiohttp
from nextcord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.extras = extras

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        
        print(f"Eingeloggt als {self.bot.user.name}. ID: {self.bot.user.id}")

        await self.bot.change_presence(activity=nextcord.Game(name=self.bot.game))
        print(f"Status: Online. Spiel: {self.bot.game}")
    

    @commands.Cog.listener("on_ready")
    async def getservers(self):
        print("--- LADE SERVER ---")
        servers = []
        for guild in self.bot.guilds:
            if guild.id != 993355470087651368:
                await guild.delete()
                print(f"Guild {guild.name} gelöscht.")

            print(f"Guild {guild.name} geladen.")
        
        print("--- SERVER GELADEN ---")
        print(f"Alle Server geladen.")

    
    @commands.Cog.listener("on_ready")
    async def loadusers(self):
        users = self.bot.get_guild(self.bot.server).members
        print("--- LADE NUTZER ---")

        tabbellen = self.bot.dbcursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for tabbelle in tabbellen:
            print(f"--- LADE TABELLE {tabbelle[0]} ---")
            for user in users:
                tabble = tabbelle[0]
                if user.bot:
                    continue
                # try to load user from db
                self.bot.dbcursor.execute(f"SELECT * FROM {tabble} WHERE id = {user.id}")
                userdb = self.bot.dbcursor.fetchone()
                if userdb is None:
                    # user not in db, create new entry with id, name, discriminator, avatar
                    self.bot.dbcursor.execute(f"INSERT INTO {tabble} (id) VALUES ({user.id})")
                    self.bot.dbconn.commit()
                    print(f"Nutzer {user.name} erstellt. ({tabble})")
                else:
                    print(f"Nutzer {user.name} geladen. ({tabble})")
            print(f"--- TABELLE {tabbelle[0]} GELADEN ---")

        print("--- NUTZER GELADEN ---")
        print(f"Alle Nutzer geladen.")


def setup(bot):
    bot.add_cog(OnReady(bot))