import discord
import os

TOKEN = os.getenv("TOKEN")
testing_servers=[809399376384229417]

bot = discord.Bot()

cogs = [
    'roll_dice',
    'loot',
    'advance',
    'injury',
    'scenario',
    'annoy_brad',
    'respond',
    'get_bounty_hunters',
    'help',
    'pawn',    
    'wandering'
]

for cog in cogs:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(TOKEN)