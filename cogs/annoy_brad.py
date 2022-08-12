from discord.ext import commands
from discord.commands import OptionChoice
import discord
from annoy_brad_logic import update_annoyance_trigger

onoff = [
    OptionChoice(name="On", value='On'), 
    OptionChoice(name="Off", value='Off') 
]

class annoy_brad(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

    @commands.slash_command(description="Toggle on or off the Annoy Brad Feature")
    async def annoy_brad(
    self,
    ctx,
    onoff: discord.Option(str, "Turn the annoyance off or on?", choices=onoff),
    ):
        await update_annoyance_trigger(ctx, ctx.author.mention, onoff)
    
def setup(bot): 
    bot.add_cog(annoy_brad(bot)) 