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
        user = self.compatible[self.position]["_id"]
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
    
    def _person(self, interaction: discord.Interaction):
        
        data1 = collection.find_one({"_id": interaction.user.id})
        
        username1 = data1["username"]
        age1 = data1["age"]
        profilepic1 = data1["profilepic"]
        description1 = data1["description"]
        games1 = data1["games"]
        gender1 = data1["gender"]
        language1 = data1["language"]

        embed1 = discord.Embed(title=username1, description=", ".join(games1))
        fields = [("Gender:", gender1, True),
                ("Age:", age1, True),
                ("Language:", ", ".join(language1), True),
                ("About me:", description1, False)]
            
        for name, value, inline in fields:
            embed1.add_field(name=name, value=value, inline=inline)
                
        embed1.set_image(url=profilepic1)
        embed1.set_footer(text="Powered by Ikigai")

        return embed1
    
    @discord.ui.button(style=discord.ButtonStyle.green, emoji="\U00002764")
    async def like(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Edit message to new person and save that person was liked in db"
        # collection.update_one({"_id": interaction.user.id}, {"$push": {"liked": self.compatible[self.position]["_id"]}})
        collection.update_one({"_id": interaction.user.id}, {"$pull": {"like": self.compatible[self.position]["_id"]}})
        
        user = self.bot.get_user(self.compatible[self.position]["_id"])
        
        if user: # In case user is not in cache we need to check if they are
            embed = self._person(interaction=interaction)
            await user.send(f"{interaction.user} liked your profile")
            await user.send(embed=embed)

        self.position += 1
        
        if self.position >= len(self.compatible):
            await interaction.message.delete()
            await interaction.response.send_message("You have view all people that liked you", ephemeral=True)
            self.stop()
        else: #Create next embed
            embed = self._new_person()

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji="\U0001f44e")
    async def dislike(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Edit message to new person"
        collection.update_one({"_id": interaction.user.id}, {"$pull": {"like": self.compatible[self.position]["_id"]}})
        self.position += 1

        
        if self.position >= len(self.compatible):
            await interaction.message.delete()
            await interaction.response.send_message("You have view all people that liked you", ephemeral=True)
            self.stop()
        else: #Create next embed
            embed = self._new_person()

            await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(emoji="\U0001f6ab")
    async def calcell(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Stops the view"
        await interaction.message.delete()
        await interaction.response.send_message("Search stopped", ephemeral=True)
        self.stop()

class MyModal(discord.ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timed_out = True    
        
    
class Likes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
            
    
    @discord.app_commands.command()
    async def likes(self, interaction: discord.Interaction):
        """Shows people who liked you"""
        name_tag = interaction.user.name
        tag =  interaction.user.discriminator
        
        collection.update_one({"_id": interaction.user.id}, {"$set": {"user_tag": f"{name_tag}#{tag}"}})
        
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return
        
        if not collection.find_one({"_id": interaction.user.id}):
            return await interaction.response.send_message("You don`t have profile yet. Use ***/setup*** to create profile.", ephemeral=True)

        userr = collection.find_one({"_id": interaction.user.id})

        user_likes = userr["like"]
        
        if not user_likes:
            return await interaction.response.send_message("You don't have any likes", ephemeral=True)

        compatible = collection.find({"_id": {"$in": user_likes}})
        
        view = YourView(self.client, list(compatible))

        await interaction.response.send_message(embed=view._new_person(), view=view)

Cog = Likes