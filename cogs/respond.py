from discord.ext import commands
from discord.commands import OptionChoice
import discord
import os
from annoy_brad_logic import annoy_brad

response_types = [
        OptionChoice(name="No", value="no"), #  Value must be a string.
        OptionChoice(name="Gimme", value="gimme"), #  Value must be a string.
        OptionChoice(name="Deal!", value="deal"), #  Value must be a string.
        OptionChoice(name="No Deal!", value="nodeal") #  Value must be a string.
    ]


class respond(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="respond to someone with a meme")
    # pycord will figure out the types for you
    async def respond(
    self,
    ctx,
    response: discord.Option(str, "Aight bitch, how you wanna respond to this fool", choices=response_types)
    ):
        cwd = os.getcwd()
        file = f'assets/images/{response}.jpg'
        location = os.path.join(cwd,file)
        brad =  await annoy_brad(ctx)
        if not brad:
            await ctx.respond(files = [discord.File(location)])
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(respond(bot)) # add the cog to the bot

