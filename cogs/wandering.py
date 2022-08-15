from discord.ext import commands
from discord.commands import OptionChoice
import discord
import os
from annoy_brad_logic import annoy_brad
import pandas as pd
import random
from insults import get_long_insult

response_types = [
        OptionChoice(name="Lawful", value="lawful"), #  Value must be a string.
        OptionChoice(name="Outlaw", value="illegal")
    ]


class wandering_trader(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="figure out what the wandering trader has to offer", name='wandering')
    # pycord will figure out the types for you
    async def wandering_trader(
    self,
    ctx,
    lawfulness: discord.Option(str, "Aight bitch, you down with the 5-0 or you living life one inch at a time?", choices=response_types)
    ):
        cwd = os.getcwd()
        file = f'assets/wandering_trader/{lawfulness}.csv'
        location = os.path.join(cwd,file)
        df = pd.read_csv(os.path.join(cwd, location))
        rolls = get_rolls(lawfulness)
        items = get_items(df, rolls)
        embed = get_embed(items)
        brad =  await annoy_brad(ctx)
        if not brad:
            await ctx.respond(embed = embed)
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(wandering_trader(bot)) # add the cog to the bot

def get_rolls(lawfulness):
    if lawfulness == 'lawful':
        roll_count = 3
    else: roll_count = 2
    rolls = []
    for i in range(roll_count):
        roll = random.randint(1,20)
        rolls.append(roll)
    return rolls
    
def get_items(df, rolls):
    items = []
    for roll in rolls:
        item = df.loc[df['roll'] == roll]['gear_text'].values[0]
        items.append(item)
    return items

def get_embed(items):
    embed = discord.Embed(
            title="Oh Shit, Wandering Trader!",
            description=f"Lets see what you got you **{get_long_insult()}**",
            color=discord.Colour.nitro_pink(), # Pycord provides a class with default colors you can choose from
        )
    i = 1
    for item in items:
        embed.add_field(name=f'Item {i}', value=f'{item}', inline=False)
        i+=1
    embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    return embed