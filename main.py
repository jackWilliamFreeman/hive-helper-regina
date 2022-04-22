from typing_extensions import Required
import discord
from discord.commands import OptionChoice
import random
import os

TOKEN = os.getenv("TOKEN")
testing_servers=[809399376384229417]

bot = discord.Bot(debug_guilds=testing_servers)

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

@bot.command()
# pycord will figure out the types for you
async def roll_dice(
    ctx, 
    number_of_dice: discord.Option(int, max_value= 99,
    description="the number of dice you want to roll"), 
    dice_size: discord.Option(int,description="the number of sides to the dice"), 
    is_distinct: discord.Option(bool, description="Do you want this set of dice to be distinct?")
    ):

    if (number_of_dice > dice_size) & is_distinct:
        await ctx.respond("OI YOU FUCKING SLUT CHOOSE A REALISTIC DISTINCT OPTION FOR FUCKS SAKE")
        return
    roll_number = 0
    rolls = []
    while roll_number < number_of_dice:
        roll = random.randint(1, number_of_dice)
        if is_distinct:
            if roll in rolls:
                continue
            else:
                rolls.append(roll)
                roll_number += 1
                continue
        rolls.append(roll)
        roll_number+=1
    
    rolls.sort()

    embed = discord.Embed(
        title="YOUR FUCKING DICE",
        description="HERE YOU GO YOU HORRIFIC TROLL",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="ROLLS:", value=f"`{rolls}`", inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/6sided_dice_%28cropped%29.jpg")
    embed.set_author(name="Hive Helper Regina", icon_url="https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B")

    await ctx.respond(embed=embed)

opening_options = [
    OptionChoice(name="Smashed it like a big boi", value="smashed"),
    OptionChoice(name="Opened it like a smart cunt", value="opened")
]

@bot.command()
async def loot(ctx,
    how_did_you_open_it: discord.Option(str, "How did you open the crate?", choices=opening_options)
    ):
    await ctx.respond(f"yo you {how_did_you_open_it} it")


class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

@bot.command()
async def flavor(ctx):
    await ctx.respond("Choose a flavor!", view=MyView())

bot.run(TOKEN)