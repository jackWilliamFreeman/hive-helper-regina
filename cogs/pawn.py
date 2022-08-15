from discord.ext import commands
from discord.commands import OptionChoice
import discord
import os
import random
import pandas as pd
from annoy_brad_logic import annoy_brad
from insults import get_long_insult

global cwd
cwd = os.getcwd()

class pawn(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="pawn to someone with a meme")
    # pycord will figure out the types for you
    async def pawn(
    self,
    ctx
    ):

        pistol = get_item('pistol')
        basic = get_item('basic')
        special = get_item('special')
        heavy = get_item('heavy')
        grenades = get_item('grenade')
        rare_mellee = get_item('rare')
        support = get_item('support')
        illegal = get_illegal()
        
        embed = get_embed(pistol, basic, special, heavy, grenades, rare_mellee, support, illegal)

        brad =  await annoy_brad(ctx)
        if not brad:
            await ctx.respond(embed=embed)

    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(pawn(bot)) # add the cog to the bot

def get_item(name):
    location = f'assets/pawn/{name}.csv'
    df = pd.read_csv(os.path.join(cwd, location))
    roll = random.randint(1, df.shape[0])
    row = df.loc[df['roll'] == roll]
    if row['has_another_roll'].values[0]:
        dice_size = row['dice_size'].values[0]
        second_roll = random.randint(1, dice_size)
        return row[f'option_{second_roll}'].values[0]
    else:
        return row['description'].values[0]

def get_illegal():
    location = f'assets/pawn/illegal.csv'
    df = pd.read_csv(os.path.join(cwd, location))
    roll = random.randint(1, df.shape[0])
    row = df.loc[df['roll'] == roll]
    return row['description'].values[0]

def get_embed(pistol, basic, special, heavy, grenades, rare_mellee, support, illegal):
    embed = discord.Embed(
            title="Pawn Shop Items",
            description=f"Lets see what you got you **{get_long_insult()}**",
            color=discord.Colour.nitro_pink(), # Pycord provides a class with default colors you can choose from
        )
    embed.add_field(name="Pistols:", value=f"{pistol}", inline=False)
    embed.add_field(name="Basic Weapons:", value=f"{basic}", inline=False)
    embed.add_field(name="Special Weapons:", value=f"{special}", inline=False)
    embed.add_field(name="Heavy Weapons:", value=f"{heavy}", inline=False)
    embed.add_field(name="Grenades:", value=f"{grenades}", inline=False)
    embed.add_field(name="Mellee Weapons:", value=f"{rare_mellee}", inline=False)
    embed.add_field(name="Support Crew:", value=f"{support}", inline=False)
    embed.add_field(name="*Illegal* Stuff:", value=f"{illegal}", inline=False)

    embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    return embed