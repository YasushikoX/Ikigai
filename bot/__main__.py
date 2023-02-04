import discord
from . import cogs
from discord.ext import commands
import logging

from bot.constants import TOKEN

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        await self.tree.sync() # Syncs slash commands on startup
           
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = MyBot(command_prefix='', intents=discord.Intents.all())

    for cog in cogs.all_cogs: # Adds all commands to the bot. Do not touch this.
        await bot.add_cog(cog.Cog(bot))

    await bot.start(TOKEN) # Runs the bot