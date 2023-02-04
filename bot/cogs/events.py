import discord

from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener() # This is @bot.event but in a cog
    async def on_ready(self):
        print('Bot is up and running under the name {0.user}'.format(self.client))
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.guild):
        if guild.system_channel:
            await  guild.system_channel.send(f"Hello!\nI'm Ikigai, a bot that helps you find new friends.\nI work only in dm's so if you wat to create your profile and search for new friends, just type **/setup** in dm's.\nIf you have any questions, feel free to join my support server: https://discord.gg/HBy6jAHG3A or use **/help** command.")
        else:
            return
        
Cog = Events