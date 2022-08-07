from turtle import title
import discord
from discord.ext import commands
from discord.commands import OptionChoice
import random
from insults import get_long_insult
import pandas as pd

import os
import sys

global roll
global advancement_table
second_roll = 0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult
regina_url = 'https://scontent.xx.fbcdn.net/v/t1.15752-9/278403172_399692048829552_6640220989778099445_n.jpg?stp=dst-jpg_s403x403&_nc_cat=101&ccb=1-5&_nc_sid=aee45a&_nc_ohc=fp1v8cyJAJwAX8OItsD&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AVJGPV02ajRAuuVrZxJxjwaIpQNKrbd1MTu_QNLywsnqsw&oe=6289995B'

options = []

advancement_style = [
        OptionChoice(name="Advancing a Ganger", value="ganger"), #  Value must be a string.
        OptionChoice(name="Advancing a Juve, Leader, Champ or Specialist", value="other") #  Value must be a string.
    ]


i = 2
denominator = '+'
while i >= -2:
    if i < 0:
        denominator = ''
    if i == 0:
        options.append(discord.SelectOption(label="Do Nothing",description="Do Not Modify", value = 0))
        i-=1
        continue
    option = discord.SelectOption(label=f'Modify by {denominator}{i}', description=f"use {abs(i * 5)} XP to modify roll", value=i)
    options.append(option)
    i-=1

class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Modify Advancement Roll?", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = options,
        disabled=False
    )

    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        selected_value = select.values[0]
        global roll
        roll = roll + int(selected_value)
        if roll > 12 or roll < 1:
            
            select.disabled=True
            await interaction.response.edit_message(view=self)
            await gctx.send(f'YOU NUMPTY! YOU MUST CHOOSE AN XP MODIFICATION THAT KEEPS IT WITHIN 12 AND 1...TRY AGAIN')
            return

        #work out where we are currently after previous selections
        current_advancement = advancement_table.loc[advancement_table['roll'] == roll]
        new_advancement_description = current_advancement['description'].values[0]
        global second_roll
        if current_advancement['has_another_roll'].values[0]: 
                dice_size = current_advancement['dice_size'].values[0]
                second_roll = random.randint(1, dice_size)
                if second_roll % 3 == 0:
                    mod_roll = 2
                else:
                    mod_roll = 1
                selected_option = current_advancement[f'option_{mod_roll}'].values[0]
        else:
                selected_option = new_advancement_description

        #they changed the roll
        if selected_value != '0':
            await interaction.message.edit(f"You have changed the roll to {roll} by adding {int(selected_value)}, this means {new_advancement_description}")
            select.disabled=True
            await interaction.response.edit_message(view=self)

            await interaction.followup.send(f'Your ganger has gained: **{selected_option}**')
        
        #they didnt change the roll and can modify further
        else:
            select.disabled=True
            await interaction.message.edit(f'Now you have selected to remain with {new_advancement_description} and have rolled a **{second_roll}**, you can modify this with xp if needed')
            await interaction.response.edit_message(view=MySecondView())

class MySecondView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = f"Modify Second Roll??", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = options,
        disabled=False,
        row=0
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled=True
        selected_value = select.values[0]
        current_advancement = advancement_table.loc[advancement_table['roll'] == roll]
        global second_roll
        if selected_value != 0:
            second_roll = second_roll + int(selected_value)
        if second_roll > 3:
            mod_roll = 2
        else:
            mod_roll = 1
        if current_advancement['has_another_roll'].values[0]:
            selected_option = current_advancement[f'option_{mod_roll}'].values[0]
        else:
            selected_option = current_advancement['description'].values[0]

        await interaction.response.edit_message(view=self)
        await interaction.message.reply(f'you got **{selected_option}**')

class advance(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="advance one of your gangers")
    # pycord will figure out the types for you
    async def advance(
    self,
    ctx,
    advancement_style: discord.Option(str, "What type of Crate was it?", choices=advancement_style)
    ):
        global gctx
        gctx = ctx
        if advancement_style == 'ganger':
            advancement_file = os.path.join(os.getcwd(),'assets/Advance_gangers.csv')
        else:
            advancement_file = os.path.join(os.getcwd(),'assets/Advance_Leaders_Champs_Spec_Juves.csv')
        global advancement_table
        advancement_table = pd.read_csv(advancement_file)

        embed = discord.Embed(
                title="Advancement Table",
                description=f"Check out the table below:",
                color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
        embed.add_field(name="Below are the rolls and their options", value="use to modify your rolls if required")
        for index, row in advancement_table.iterrows():
            embed.add_field(name=row['roll'], value=row['description'], inline=False)
        embed.set_author(name="Hive Helper Regina", icon_url=regina_url)
        embed.set_thumbnail(url=regina_url)
        global roll
        roll=random.randint(2,12)
        current_advance = advancement_table.loc[advancement_table['roll'] == roll]['description'].values[0]

        await ctx.send("here is the advancement table:", embed=embed)
        await ctx.send(f"You have rolled a **{roll}**, currently that means {current_advance}\r\nYou can use XP to modify the roll",view=MyView(timeout=25))
    

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(advance(bot)) # add the cog to the bot

