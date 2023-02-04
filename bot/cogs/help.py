import discord
from discord.ext import commands


class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interaction: discord.Interaction = None
    
    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        self.interaction = interaction

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client      
        
    @discord.app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """Shows command list and info about bot"""
        
        embed = discord.Embed(title="Commands and Information", color=discord.Color.blue())
        fields = [("Commands:", "***/start*** - Gives general info at the start\n***/setup*** - Creates/changes profile\n***/search*** - Searches for user with same games\n ***/likes*** - Shows people that liked your profile and lets you like them back\n ***/profile*** - Shows your profile\n***/deleteprofile*** - Deletes your profile", False),
                  ("Links:", "Add bot: https://goo.su/h1i1\nSuport server: https://discord.gg/hnCQAfJS\n Git hub page: https://github.com/YasushikoX\nBuy me a coffee: https://www.buymeacoffee.com/yasushiko\nTop.gg: https://top.gg/bot/1016513838486655026?s=03421e08dc12d", False),
                  ("Info:", "This bot is still in development. If you have any suggestions or found a bug, please submit it on discord server.", False)]
            
        for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                
        embed.set_footer(text="Powered by Ikigai")
        
        await interaction.response.send_message(embed=embed)

Cog = Help