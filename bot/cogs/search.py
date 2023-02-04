import discord
from discord.ext import commands
from pymongo import MongoClient
import random
from typing import List

from bot.constants import collection
 
class YourView(discord.ui.View):
    def __init__(self, bot: commands.Bot, compatibale: List[dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.compatible = compatibale
        self.position = 0   

    def _new_person(self):
        "Create new embed with new person"
        username = self.compatible[self.position]["username"]
        age = self.compatible[self.position]["age"]
        profilepic = self.compatible[self.position]["profilepic"]
        description = self.compatible[self.position]["description"]
        gender = self.compatible[self.position]["gender"]
        games = self.compatible[self.position]["games"]
        language = self.compatible[self.position]["language"]

        embed = discord.Embed(title=username, description=", ".join(games))
        fields = [("Gender:", gender, True),
                ("Age:", age, True),
                ("Language:", ", ".join(language), True),
                ("About me:", description, False)]
            
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
                
        embed.set_image(url=profilepic)
        embed.set_footer(text="Powered by Ikigai")

        return embed

    @discord.ui.button(style=discord.ButtonStyle.green, emoji="\U00002764")
    async def like(self, interaction: discord.Interaction, button: discord.ui.Button):
        collection.update_one({"_id": self.compatible[self.position]["_id"]}, {"$push": {"like": interaction.user.id}})
        
        user = self.bot.get_user(self.compatible[self.position]["_id"])
        if user: # In case user is not in cache we need to check if they are
            await user.send(f"Someone liked you profile use ***/likes*** to see who liked you.")

        if interaction.user.id in self.compatible[self.position]["like"]:
            self.position += 1

            if self.position >= len(self.compatible):
                await interaction.message.delete()
                await interaction.response.send_message("There are no more profiles you have not yet viewed", ephemeral=True)
                self.stop()
            else: #Create next embed
                if interaction.user.id == self.compatible[self.position]["_id"]:
                    self.position += 1
                    if self.position >= len(self.compatible):

                        await interaction.message.delete()
                        await interaction.response.send_message("There are no more profiles you have not yet viewed", ephemeral=True)
                        self.stop()
                    else:
                        embed = self._new_person()

                        await interaction.response.edit_message(embed=embed, view=self)
                else:
                    embed = self._new_person()

                    await interaction.response.edit_message(embed=embed, view=self)
        else: 

            self.position += 1

            if self.position >= len(self.compatible):
                await interaction.message.delete()
                await interaction.response.send_message("There are no more profiles you have not yet viewed", ephemeral=True)
                self.stop()
            else: #Create next embed
                if interaction.user.id == self.compatible[self.position]["_id"]:
                    self.position += 1
                    embed = self._new_person()

                    await interaction.response.edit_message(embed=embed, view=self)
                else:
                    embed = self._new_person()

                    await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji="\U0001f44e")
    async def dislike(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.position += 1

        if self.position >= len(self.compatible):
            await interaction.message.delete()
            await interaction.response.send_message("There are no more profiles you have not yet viewed", ephemeral=True)
            self.stop()
        else: #Create next embed
            if interaction.user.id == self.compatible[self.position]["_id"]:
                    self.position += 1
                    if self.position >= len(self.compatible):
                        await interaction.message.delete()
                        await interaction.response.send_message("There are no more profiles you have not yet viewed", ephemeral=True)
                        self.stop()
                    else:
                        embed = self._new_person()

                        await interaction.response.edit_message(embed=embed, view=self)
            else:
                embed = self._new_person()

                await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(emoji="\U0001f6ab")
    async def calcell(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message("Search stopped", ephemeral=True)
        self.stop()

class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timed_out = True    
        
    
class Search(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
            
    
    @discord.app_commands.command()
    async def search(self, interaction: discord.Interaction):
        """Search for people with same interests as you"""

        name_tag = interaction.user.name
        tag =  interaction.user.discriminator
        
        collection.update_one({"_id": interaction.user.id}, {"$set": {"user_tag": f"{name_tag}#{tag}"}})
        
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return
        
        if not collection.find_one({"_id": interaction.user.id}):
            return await interaction.response.send_message("You don`t have profile yet. Use ***/setup*** to create profile.", ephemeral=True)
        
        user = collection.find_one({"_id": interaction.user.id})

        if not "games" in dict(user):
            return await interaction.response.send_message("You don`t have games in your profile. Use ***/games*** to add games.", ephemeral=True)
        
        if not "language" in dict(user):
            return await interaction.response.send_message("You don`t have language in your profile. Use ***/language*** to set up language.", ephemeral=True)

        user_games = user["games"]
        
        compatiblee = collection.find({"games": {"$in": user_games}})
        
        compatible = list(compatiblee)
        random.shuffle(compatible)
        
        if not compatible:
            return await interaction.response.send_message("There are no compatible profiles", ephemeral=True)
        
        view = YourView(self.client, list(compatible))

        await interaction.response.send_message(embed=view._new_person(), view=view)

Cog = Search 