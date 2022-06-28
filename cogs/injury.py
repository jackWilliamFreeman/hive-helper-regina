import discord
from discord.ext import commands
import random
from insults import get_long_insult
import pandas as pd

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
global roll

from insults import get_long_insult, get_short_insult

class injury(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command()
    # pycord will figure out the types for you
    async def injury(
    self,
    ctx
    ):

        ten_roll = random.randint(1, 6) * 10
        single_roll = random.randint(1, 6)
        roll = ten_roll+single_roll

        injury_table = pd.read_csv('assets\injuries\Lasting_Injury_table.csv', encoding='cp1252')
        rolled_injury = injury_table.loc[injury_table['roll'] == roll]
        injury_text = rolled_injury['description'].values[0]

        embed = discord.Embed(
            title="UH OH SPAGHETTIO",
            description=f"You rolled a **{roll}**",
            color=discord.Colour.dark_gold(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="Injury:", value=f"`{injury_text}`", inline=False)
        embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
        embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")

        await ctx.respond(embed=embed)
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(injury(bot)) # add the cog to the bot

