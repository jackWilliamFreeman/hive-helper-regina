from typing_extensions import Required
import discord
from discord.commands import OptionChoice, SlashCommandGroup
import os
from insults import get_long_insult, get_short_insult

TOKEN = os.getenv("TOKEN")
testing_servers=[809399376384229417]

bot = discord.Bot(debug_guilds=testing_servers)

cogs = [
    'roll_dice',
    'loot',
    'advance'
]

for cog in cogs:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(TOKEN)