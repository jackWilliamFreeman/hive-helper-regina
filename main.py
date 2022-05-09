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

@bot.command(name = "embed_test", description = "test writing an embedded post")
async def test1(ctx):
    embed = discord.Embed(
        title="My Amazing Embed",
        description="Embeds are super easy, barely an inconvenience.",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="A Normal Field", value="A really nice field with some information. **The description as well as the fields support markdown!**", inline=False)

    embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
    embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
    embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)
 
    embed.set_footer(text="Footer! No markdown here.") # footers can have icons too
    embed.set_author(name="Pycord Team", icon_url="https://images.theconversation.com/files/186154/original/file-20170915-16324-153bs7v.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip")
    embed.set_thumbnail(url="https://images.theconversation.com/files/186154/original/file-20170915-16324-153bs7v.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip")
    embed.set_image(url="https://images.theconversation.com/files/186154/original/file-20170915-16324-153bs7v.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip")
 
    await ctx.respond("Hello! Here's a cool embed.", embed=embed) # Send the embed with some text

@bot.command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.command()
# pycord will figure out the types for you
async def add(ctx, first: discord.Option(int), second: discord.Option(int)):
  # you can use them as they were actual integers
  sum = first + second
  await ctx.respond(f"The sum of {first} and {second} is {sum}.")

valid_ranks = [
    OptionChoice(name="Bronze", value="Bronze"), #  Value must be a string.
    OptionChoice(name="Silver", value="Silver"), #  Value must be a string.
    OptionChoice(name="Diamond", value="Diamond") #  Value must be a string.
]

@bot.command(name = "choice_test", description = "choose options")
async def choice_test(ctx, rank: discord.Option(str, "what is yo rank", choices=valid_ranks)):
  await ctx.respond(rank)


opening_options = [
    OptionChoice(name="Smashed it like a big boi", value="smashed"),
    OptionChoice(name="Opened it like a smart cunt", value="opened")
]

bot.run(TOKEN)