import discord
from discord.ext import commands
import random
from insults import get_long_insult
from annoy_brad_logic import annoy_brad
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult, get_short_insult

class roll_dice(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="roll some dice")
    # pycord will figure out the types for you
    async def roll_dice(
    self,
    ctx, 
    number_of_dice: discord.Option(int, max_value= 99,
    description="the number of dice you want to roll"), 
    dice_size: discord.Option(int,description="the number of sides to the dice"), 
    is_distinct: discord.Option(bool, description="Do you want this set of dice to be distinct?")
    ):

        if (number_of_dice > dice_size) & is_distinct:
            await ctx.respond(f"OI! You {get_long_insult()}, You cant choose more dice then possible distinct options")
            return
        rolls = get_dice_rolls(number_of_dice, dice_size, is_distinct)
    
        rolls.sort()

        embed = discord.Embed(
            title="YOUR FUCKING DICE",
            description=f"Here you go you **{get_long_insult().upper()}**",
            color=discord.Colour.dark_gold(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="ROLLS:", value=f"`{rolls}`", inline=False)
        embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
        embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
        brad =  await annoy_brad(ctx)
        if not brad:
            await ctx.respond(embed=embed)
    
def get_dice_rolls(number_of_dice, dice_size, is_distinct):
    roll_number = 0
    rolls = []
    while roll_number < number_of_dice:
        roll = random.randint(1, dice_size)
        if is_distinct:
            if roll in rolls:
                continue
            else:
                rolls.append(roll)
                roll_number += 1
                continue
        rolls.append(roll)
        roll_number+=1
    return rolls

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(roll_dice(bot)) # add the cog to the bot

