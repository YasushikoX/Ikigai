import discord
from discord.ext import commands


class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interaction: discord.Interaction = None
    
    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        self.interaction = interaction

class Start(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client      
        
    @discord.app_commands.command(name="start")
    async def start(self, interaction: discord.Interaction):
        """Sets up your profile or changes your profile"""
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return
        
        await interaction.response.send_message("Hello and welcome to Ikigai.\nThis bot will help you with finding teammates.\nTo continue with profile set up use command ***/setup***\nUse ***/help*** to get  command list and other helpful information.", ephemeral=True)
        
Cog = Start
        