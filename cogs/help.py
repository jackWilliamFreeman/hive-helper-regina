from discord.ext import commands
import discord
from annoy_brad_logic import annoy_brad
from insults import get_long_insult


class help(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="Get some Help")
    # pycord will figure out the types for you
    async def help(
    self,
    ctx
    ):
        brad =  await annoy_brad(ctx)

        embed = discord.Embed(
            title="Help",
            description=f"Alright listen up you **{get_long_insult().upper()}**, things work differently now. Each command is started by just typing the slash key '/'. The options are below",
            color=discord.Colour.dark_purple(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="Help", value=f"You literally just pressed this you {get_long_insult()}", inline=False)
        embed.add_field(name="Injury", value=f"gets you a random injury for some poor sod", inline=False)
        embed.add_field(name="Loot", value=f"Now we are talking...gets the loot for a dude, sometimes they die", inline=False)
        embed.add_field(name="Respond", value=f"Gives you an image to respond to someone with, a picture can be worth a thousand words..", inline=False)
        embed.add_field(name="Get_bounty_hunters", value=f"Gets you a bounty hunter...maybe even me", inline=False)
        embed.add_field(name="Annoy_Brad", value=f"a switch that can turn off or on the wonderful Brad annoyance feature", inline=False)
        embed.add_field(name="Advance", value=f"Advance a ganger", inline=False)
        embed.add_field(name="Scenario", value=f"Get a random scenario", inline=False)
        embed.add_field(name="Roll", value=f"Roll some magic dice", inline=False)

        embed.set_thumbnail(url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")
        embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B") 
        if not brad:
            await ctx.respond(embed = embed)
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(help(bot)) # add the cog to the bot

