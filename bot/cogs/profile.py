import discord
from discord.ext import commands
from pymongo import MongoClient
from bot.constants import collection

class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timed_out = True    
        
    
class Profile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @discord.app_commands.command()
    async def profile(self, interaction: discord.Interaction):
        """Shows your profile"""
        await interaction.response.send_message("Loading...", ephemeral=True)
        
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return
        
        data = collection.find_one({"_id": interaction.user.id})

        if not data:
            return await interaction.response.send_message("You don`t have profile yet. Use ***/setup*** to create profile.", ephemeral=True)
        
        if not "games" in data:
            return await interaction.response.send_message("You don`t have games in your profile. Use ***/games*** to add games.", ephemeral=True)
        
        if not "language" in data:
            return await interaction.response.send_message("You don`t have language in your profile. Use ***/language*** to set up language.", ephemeral=True)
        
        username = data["username"]
        age = data["age"]
        profilepic = data["profilepic"]
        description = data["description"]
        games = data["games"]
        gender = data["gender"]
        language = data["language"]
        
        embed = discord.Embed(title=username, description=", ".join(games))
        fields = [("Gender:", gender, True),
                ("Age:", age, True),
                ("Language:", ", ".join(language), True),
                ("About me:", description, False)]
            
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            
        embed.set_image(url=profilepic)
        embed.set_footer(text="Powered by Ikigai")
        
        
        await interaction.channel.send(embed=embed)
        
Cog = Profile