import discord
from discord.ext import commands
from pymongo import MongoClient
from bot.constants import collection

class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timed_out = True    
    
    
class Deleteprofile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client   
        
    @discord.app_commands.command()
    async def deleteprofile(self, interaction: discord.Interaction):
        """Deletes your profile"""
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return

        if not collection.find_one({"_id": interaction.user.id}):
            return await interaction.response.send_message("You don`t have profile yet. Use ***/setup*** to create profile.", ephemeral=True)

        collection.delete_one({"_id": interaction.user.id})

        await interaction.response.send_message("Your profile have been deleted", ephemeral=True)
        
Cog = Deleteprofile