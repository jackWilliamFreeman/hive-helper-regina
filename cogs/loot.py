import discord
from discord.ext import commands
from discord.commands import OptionChoice
import random
import pandas as pd
from insults import get_long_insult

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult, get_short_insult

class loot(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    loot_crate_type = [
        OptionChoice(name="Gold", value="gold"), #  Value must be a string.
        OptionChoice(name="Silver", value="silver"), #  Value must be a string.
        OptionChoice(name="Vox Comms", value="vox Comms") #  Value must be a string.
    ]

    opening_method = [
        OptionChoice(name="Opening it like a smarty", value="opened"), #  Value must be a string.
        OptionChoice(name="FUCKING SMASHED IT, YEH!", value="smashed") #  Value must be a string.
    ]

    @commands.slash_command()
    # pycord will figure out the types for you
    async def get_loot(
    self,
    ctx, 
    crate_type: discord.Option(str, "What type of Crate was it?", choices=loot_crate_type),
    opening_type: discord.Option(str, "What type of Crate was it?", choices=opening_method)
    ):

        loot = get_loot(crate_type, opening_type)

        embed = discord.Embed(
            title="YOUR FUCKING DICE",
            description=f"Here you go you **{get_long_insult().upper()}**",
            color=discord.Colour.dark_gold(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="ROLLS:", value=f"`{rolls}`", inline=False)
        embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
        embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")

        await ctx.respond(embed=embed)



get_randomn_loot(crate_type, roll, has_range, dice_size)

def get_randomn_loot(crate_type, roll, has_range, dice_size):
    df = pd.read_csv("loot_rolls.csv", encoding='cp1252')
    print(df)

    dice_roll = random.randint(1,dice_size)

    selected=''
    if has_range:
        selected = df.loc[
        (df['roll'] == roll)
        & (df['crate_type'] == crate_type) 
        & (df['low_range'] <= dice_roll)
        & (df['high_range'] >= dice_roll)]
    else:
        selected = df.loc[
        (df['roll'] == roll)
        & (df['crate_type'] == crate_type) 
        & (df['absolute'] == dice_roll)]

    treasure = selected['value'].values[0]  

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(loot(bot)) # add the cog to the bot

