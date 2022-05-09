import discord
from discord.ext import commands
import random
from insults import get_long_insult

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult

options = []


i = 10
denominator = '+'
while i >= -10:
    if i < 0:
        denominator = ''
    if i == 0:
        options.append(discord.SelectOption(label="Do Nothing",description="Use 0 Xp to Modify", value = 0))
        i-=1
        continue
    option = discord.SelectOption(label=f'Modify by {denominator}{i}', description=f"use {abs(i)} XP to modify roll", value=i)
    options.append(option)
    i-=1

class MySecondView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Modify Second Roll??", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = options,
        disabled=False,
        row=0
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled=True
        
        await interaction.response.edit_message(view=self)
        await interaction.message.reply("good roll cnt")


class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Modify Advancement Roll?", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = options,
        disabled=False
    )

    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled=True
        selected_value = select.values[0]
        if selected_value != '0':
            await interaction.message.edit("Selection Complete")
            await interaction.response.edit_message(view=self)
            await interaction.followup.send('nice choice')
            
        else:
            await interaction.message.edit("Now do you want to spend xp on the second roll?")
            await interaction.response.edit_message(view=MySecondView())

class advance(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command()
    # pycord will figure out the types for you
    async def advance(
    self,
    ctx
    ):
        roll=random.randint(2,12)
        await ctx.respond(f"Here is the Advance table, you rolled a {roll}",view=MyView(timeout=25))
    

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(advance(bot)) # add the cog to the bot

