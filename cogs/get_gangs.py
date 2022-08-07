import discord
from discord.ext import commands
import random
from insults import get_long_insult
import bs4
from bs4 import BeautifulSoup
import requests
from discord.commands import OptionChoice


import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from insults import get_long_insult, get_short_insult

CAMPAIGN_URL = "https://yaktribe.games/underhive/campaign/hive_hustle_outcast_campaign.11244/"

class Ganger:
    def __init__(self, name = None, ganger_type = None, cost = None):
        self.name = name,
        self.ganger_type = ganger_type,
        self.cost = cost

def get_gangs(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    gangs = {}

    for element in soup.find_all('div', class_ ='col mb-4'):
        for section in element:
            if isinstance(section, bs4.element.NavigableString) and not section.isspace():
        #ganger_name
                gang_name = section
        url = element.find('a', href=True)
        url_text = f'https://yaktribe.games/{url["href"]}'
        gangs[url.text] = url_text
    return gangs

gangs = get_gangs(CAMPAIGN_URL)

gang_choices = []

for gang in gangs:
    gang_choices.append(OptionChoice(name=f'{gang}', value=f'{gangs[gang]}'))

class get_gangs(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command()
    # pycord will figure out the types for you
    async def get_gangs(
    self,
    ctx, 
    gang_one: discord.Option(str, "Which Gang??", choices=gang_choices),
    gang_two: discord.Option(str, "Which Gang??", choices=gang_choices)
        ):
        await ctx.defer()
        try:
            gang_one = get_gang_list(gang_one)
            gang_two = get_gang_list(gang_two)
            chat = f'Gang at {gang_one} has folling members:'
            for ganger in gang_one:
                chat = chat + f'\r\nName {ganger.name} : Cost: {ganger.cost} : Hanger On?: {ganger.is_hanger_on} : In Recovery? : {ganger.in_recovery}'
            await ctx.followup.send(chat)
        except Exception as e:
            await ctx.followup.send(f'error: {e}')

    
def get_gang_list(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    gang = []
    for ganger_card in soup.find_all('div', class_ = 'ganger-parent ganger-order-check'):
        ganger = Ganger()
        hanger_on = ganger_card.find_all("div", class_ = "hiredgun-badge")
        if hanger_on:
            ganger.is_hanger_on = True
        else:
            ganger.is_hanger_on = False

        in_recovery = ganger_card.find_all('i', class_ = 'fa fa-medkit fa-lg ml-2')
        if in_recovery:
            ganger.in_recovery = True
        else: ganger.in_recovery = False

        title_cards = ganger_card.find_all("h5", class_ = "d-md-inline-block")
        for card in title_cards:
            for section in card:
                if isinstance(section, bs4.element.NavigableString) and not section.isspace():
                #ganger_name
                    ganger.name = section

            ganger_type = card.find('small', class_='ml-2')
        #ganger_type
            ganger.ganger_type = ganger_type.text
        cost_section = ganger_card.find_all('div', class_ = 'gang-ganger-cost')
        for section in cost_section:
        #ganger cost 
            ganger.cost = int(section.text.replace('Credits',''))
        
        gang.append(ganger)
    return gang

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(get_gangs(bot)) # add the cog to the bot

