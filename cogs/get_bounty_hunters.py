from discord.ext import commands
from discord.commands import OptionChoice
import discord
import os
import random
from annoy_brad_logic import annoy_brad
import pandas as pd
from insults import get_long_insult


lawfulness = [
        OptionChoice(name="Lawful", value="lawful"), #  Value must be a string.
        OptionChoice(name="Outlaw", value="outlaw")
    ]


class get_bounty_hunters(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="get your own hunter of bounties!", name='bounty_hunter')
    # pycord will figure out the types for you
    async def get_bounty_hunters(
    self,
    ctx,
    law: discord.Option(str, "You follow the law or you above it?", choices=lawfulness)
    ):
        cwd = os.getcwd()
        file = f'assets/bounty_hunters/bounty_hunters.csv'
        location = os.path.join(cwd,file)
        brad =  await annoy_brad(ctx)
        if not brad:
            df = pd.read_csv(location, encoding='cp1252')
            hunters = df.loc[df['hunter_type'] == law]
            roll = random.randint(1,12)
            hunter = hunters.loc[hunters['roll'] == roll]['description'].values[0]
            embed = get_embed(hunter)
            await ctx.respond(f'See below which bounty hunter has turned up ya {get_long_insult()}:',embed = embed)
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(get_bounty_hunters(bot)) # add the cog to the bot

def get_embed(hunter):
    embed = discord.Embed(
            title=f"{hunter}",
            description=f"Maybe this one will help you not suck?",
            color=discord.Colour.dark_teal(), # Pycord provides a class with default colors you can choose from
        )
    embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
    return embed