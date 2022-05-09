import discord
from discord.ext import commands
from discord.commands import OptionChoice
import random
import pandas as pd


import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult

regina_url = 'https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B'

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
        if opening_type=='smashed':
            single_roll = random.randint(1,3)
        else:
            single_roll = random.randint(1,6)
        ten_roll = random.randint(1,6)*10
        roll = single_roll+ten_roll

        primary, secondary = get_loot(roll, crate_type)

        title = primary['title'].values[0]
        description = primary['description'].values[0]
        
        if primary['roll_required'].values[0] == 0:
            
            embed = discord.Embed(
                title="Loot Roll!",
                description=f"Congrats, you rolled a **{roll}**",
                color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
            embed.add_field(name=title, value=description, inline=False)
            embed.set_footer(text=f"Now sod off you {get_long_insult()}") # footers can have icons too
            embed.set_author(name="Hive Helper Regina", icon_url=regina_url)
            embed.set_thumbnail(url=regina_url)
            embed.set_image(url="https://i.pinimg.com/736x/33/43/6e/33436ed730d351a6278d9fd2940af70d--warhammer-k-weapons.jpg")

            await ctx.respond(embed=embed)
        else:
            secondary_treasure = secondary['value'].values[0]
            embed = discord.Embed(
                title="Loot Roll!",
                description=f"Congrats, you rolled a **{roll}**",
                color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
            embed.add_field(name=title, value=f"-------------------------------------------\r\nyou win: **{secondary_treasure}**", inline=False)
            embed.set_footer(text=f"Now sod off you {get_long_insult()}") # footers can have icons too
            embed.set_author(name="Hive Helper Regina", icon_url=regina_url)
            embed.set_thumbnail(url=regina_url)
            embed.set_image(url="https://i.pinimg.com/736x/33/43/6e/33436ed730d351a6278d9fd2940af70d--warhammer-k-weapons.jpg")

            await ctx.respond(embed=embed)

def get_loot(roll, crate_type):
    primary_loot = get_primary_loot(roll, crate_type)
    secondary_loot = ''
    if primary_loot['roll_required'].values[0] == 1:
        dice_size = primary_loot['dice_size'].values[0]
        has_range = primary_loot['has_range'].values[0]
        secondary_loot = get_randomn_loot(crate_type, roll, has_range, dice_size)

    return primary_loot, secondary_loot

def get_primary_loot(roll, crate_type):
    df = pd.read_csv("assets/loot_rolls.csv", encoding='cp1252')

    selected = df.loc[
        (df['roll'] == roll)
        & (df['crate_type'] == crate_type)
    ]

    return selected

def get_randomn_loot(crate_type, roll, has_range, dice_size):
    df = pd.read_csv("assets/loot_rolls_secondary.csv", encoding='cp1252')

    dice_roll = random.randint(1,dice_size)

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

    return selected

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(loot(bot)) # add the cog to the bot

