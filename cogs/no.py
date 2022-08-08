from discord.ext import commands

class no(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="say no to someone")
    # pycord will figure out the types for you
    async def no(
    self,
    ctx
    ):

        await ctx.respond("fuck off brad")
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(no(bot)) # add the cog to the bot