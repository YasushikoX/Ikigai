import discord
from discord.ui import Select, View
from discord.ui import View
from discord.ext import commands
from pymongo import MongoClient
from bot.constants import collection
import asyncio
from better_profanity import profanity

class MyModal(discord.ui.Modal):
    
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timed_out = True
        self.client = client


    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not collection.find_one({"_id": interaction.user.id}):
            collection.insert_one({"_id": interaction.user.id})

        # This check makes sure the wait_for only triggers when the command user sends a message with an attachment
        def check(m: discord.Message) -> bool:
            return m.author == interaction.user and m.attachments

        await interaction.response.send_message("Please send the image you want to set as a profile picture!")

        try:
            message = await self.client.wait_for("message", check=check, timeout=86400)
        except asyncio.TimeoutError:
            return await interaction.channel.send("Failed to send image in time. Aborting.")

        profilepic = message.attachments[0].url
        collection.update_one({"_id": interaction.user.id}, {"$set": {"profilepic": profilepic}})
        
        games = Select(
                placeholder="Select games that you play",
                min_values=1,
                max_values=11,
                options=[
                discord.SelectOption(label="Valorant", emoji="<:valorantremovebgpreview:1045130612673097758>"),
                discord.SelectOption(label="League Of Legends", emoji="<:lolmin:1045131190115508325>"),
                discord.SelectOption(label="Minecraft",emoji="<:minecraft1logopngtransparentmin:1045133111463252088>" ),
                discord.SelectOption(label="Apex Legends", emoji="<:apexremovebgpreview:1045130613683929108>"),
                discord.SelectOption(label="Sea of Thives", emoji="<:seaofthieves:1045130617605607474>"),
                discord.SelectOption(label="CS GO", emoji="<:counterstrikesymbolpnglogo11:1045133537147363338>"),
                discord.SelectOption(label="Rust", emoji="<:rustdiscordemojirustlogo11563630:1053785023561613443>"),
                discord.SelectOption(label="Overwatch 2", emoji="<:Overwatch_2_logo:1053783781774999613>"),
                discord.SelectOption(label="Fortnite", emoji="<:FortniteLogo:1053823606557245531>"),
                discord.SelectOption(label="Rainbow Six Siege", emoji="<:4394393598_siegelogorainbowsixsi:1053823604393005056>"),
                discord.SelectOption(label="Chatting", emoji="<:1380370:1053824151950991441>"),
                ])
            
        async def my_callback_games(interaction: discord.Interaction):
                await interaction.message.delete()  
                collection.update_one({"_id": interaction.user.id}, {"$set": {"games": games.values}})
                language = Select(
                    placeholder="Select your languages",
                    min_values=1,
                    max_values=7,
                    options=[
                    discord.SelectOption(label="English"),
                    discord.SelectOption(label="French"),
                    discord.SelectOption(label="Russian"),
                    discord.SelectOption(label="Spanish"),
                    discord.SelectOption(label="Chinese"),
                    discord.SelectOption(label="German"),
                    discord.SelectOption(label="Japanese"),
                    ])
                        
                
                async def my_callback_language(interaction: discord.Interaction):
                    await interaction.message.delete()  
                    await interaction.channel.send("Profile have been successfully created. If you want to see it use ***/profile*** otherwise use ***/search*** to find people with same interests as you.")
                    collection.update_one({"_id": interaction.user.id}, {"$set": {"language": language.values}})
                
                language.callback = my_callback_language
                
                view = View()
                view.add_item(language)
                
                await interaction.channel.send(view=view)
        
            
        games.callback = my_callback_games
            
        view = View()
        view.add_item(games)
            
        await interaction.channel.send(view=view)
        self.timed_out = False

class Setup(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @discord.app_commands.command()
    async def setup(self, interaction: discord.Interaction):
        """Creates/updates your profile"""
        if interaction.guild:
            await interaction.user.send("This bot works only in dm's. Please use this command in here <3")
            return
        
        name_tag = interaction.user.name
        tag =  interaction.user.discriminator

        modal = MyModal(self.client, title="Create profile")
        name = discord.ui.TextInput(label="What is your name?", placeholder="John Doe")
        age =  discord.ui.TextInput(label="What is your age?", placeholder="18")
        gender = discord.ui.TextInput(label="What is your gender?", placeholder="Male♂️")
        description = discord.ui.TextInput(label="Tell about yourself", placeholder="I am a cool person")
        modal.add_item(name).add_item(gender).add_item(age).add_item(description)
        
        await interaction.response.send_modal(modal)
        
        await modal.wait()

        if modal.timed_out:
            return
        
        if age.value.isdigit():
            age_b = age.value
        else:
            await interaction.channel.send("⚠️⚠️⚠️**Your age must be a number. For now it will be set to 18.**⚠️⚠️⚠️")
            age_b = 18
        
        name_c = profanity.censor(name.value, "*")
        age_c = profanity.censor(age_b, "*")
        gender_c = profanity.censor(gender.value, "*")
        description_c = profanity.censor(description.value, "*")
        
        collection.update_one({"_id": interaction.user.id}, {"$set": {"username": name_c, "user_tag": f"{name_tag}#{tag}", "age": age_c, "gender": gender_c, "description": description_c, "like": []}})
        
        if profanity.contains_profanity(f"{name.value} , {age.value} , {gender.value} , {description.value}"):
            await interaction.channel.send("⚠️⚠️⚠️**Your profile contains bad words. Please change it. For now they have been blurred.**⚠️⚠️⚠️")

Cog = Setup