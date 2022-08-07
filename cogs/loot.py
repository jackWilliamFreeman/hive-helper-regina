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

class loot_results():
    def __init__(self, description, has_secondary_text, second_roll, secondary_text):
        self.description = description
        self.has_secondary_text = has_secondary_text
        self.second_roll = second_roll
        self.secondary_text = secondary_text

regina_url = 'https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B'

class loot(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    loot_crate_type = [
        OptionChoice(name="Gold", value="Gold"), #  Value must be a string.
        OptionChoice(name="Silver", value="Silver"), #  Value must be a string.
        OptionChoice(name="Vox Comms", value="Vox") #  Value must be a string.
    ]

    opening_method = [
        OptionChoice(name="Opening it like a smarty", value="opened"), #  Value must be a string.
        OptionChoice(name="FUCKING SMASHED IT, YEH!", value="smashed") #  Value must be a string.
    ]

    @commands.slash_command(description="get some rando loot")
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

        loot_results = await get_loot_results(roll, crate_type, ctx)
        text = loot_results.description
        if loot_results.has_secondary_text:
            text = text + f'\r\nYou then rolled a **{loot_results.second_roll}** and won: **{loot_results.secondary_text}**'
        embed = discord.Embed(
                title="Loot Roll!",
                description=f"Congrats, you rolled a **{roll}**",
                color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
        embed.add_field(name='You won:', value=text, inline=False)
        embed.set_footer(text=f"Now sod off you {get_long_insult()}") # footers can have icons too
        embed.set_author(name="Hive Helper Regina", icon_url=regina_url)
        embed.set_thumbnail(url=regina_url)
        embed.set_image(url="https://i.pinimg.com/736x/33/43/6e/33436ed730d351a6278d9fd2940af70d--warhammer-k-weapons.jpg")
        await ctx.respond(embed=embed)




async def get_loot_results(roll, crate_type, ctx):
    try:
        crate_file_rel = f'assets/{crate_type}_loot_crates.csv'
        crate_file = os.path.join(os.getcwd(),crate_file_rel)
        df = pd.read_csv(crate_file, encoding='cp1252')
        dice = 0
        result = df.loc[df['roll'] == roll]
        description = result['description'].values[0]
        has_second_roll = result['has_another_roll'].values[0]
        secondary_text = ''
        if has_second_roll:
            dice = random.randint(1,result['dice_size'].values[0])
            secondary_text = result[f'option_{dice}'].values[0]
        rolled_result = loot_results(description,has_second_roll, dice, secondary_text)
        return rolled_result
    except Exception as e:
        await ctx.respond(f'Somefink went wrong {str(e)}')

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(loot(bot)) # add the cog to the bot

