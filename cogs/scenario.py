import random
from discord.ext import commands
import discord
import os
import pandas as pd
import traceback
from annoy_brad_logic import annoy_brad
import requests
import bs4
from bs4 import BeautifulSoup
from discord.commands import OptionChoice

CAMPAIGN_URL = "https://yaktribe.games/underhive/campaign/hive_hustle_outcast_campaign.11244/"

global cwd
cwd = os.getcwd()

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
    gang_choices.append(OptionChoice(name=f'{gang}', value=f'{gang}'))

class get_scenario(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(description="say no to someone")
    # pycord will figure out the types for you
    async def get_scenario(
    self,
    ctx,
    first_gang: discord.Option(str, "Which Gang??", choices=gang_choices),
    second_gang: discord.Option(str, "Which Gang??", choices=gang_choices)
    ):
        try:
            scenario = get_scenario_df()      
            badland_scenario = get_badland_event()
            traps = get_traps(scenario)
            loot_crate = get_loot_crate(scenario)
            monster = get_monster_roll(scenario)
            local_juves = get_local_juves(scenario)
            local_denizens = get_local_denizens(scenario)
            hive_dwellers = get_hive_dwellers(scenario)
            convoy = get_convoy(scenario)
            attacker = determine_attacker(first_gang, second_gang)
            attacker_crew_method = scenario['attacker_crew_selection_method'].values[0]
            defender_crew_method = scenario['defender_crew_selection_method'].values[0]
            attacker_crew_size = get_crew_size(scenario, 'attacker')
            defender_crew_size = get_crew_size(scenario, 'defender')
            attacker_reinforcement = scenario['attacker_reinforcements'].values[0]
            defender_reinforcement = scenario['defender_reinforcements'].values[0]
            embed = get_embed(first_gang, second_gang, scenario, badland_scenario, traps, loot_crate, monster, local_juves, local_denizens, hive_dwellers, convoy, attacker, attacker_crew_method, defender_crew_method, attacker_crew_size, defender_crew_size, attacker_reinforcement, defender_reinforcement)
            
            brad =  await annoy_brad(ctx)
            if not brad:
                await ctx.respond(f"Listen up {first_gang} and {second_gang}, your scenario details are below:", embed = embed)
        except Exception as e:
            await ctx.respond(f'uh oh i got a brain problem, someone tell Jack, its:\r\n\r\n{e}{traceback.print_exc()}')
    
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(get_scenario(bot)) # add the cog to the bot

def get_badland_event():
    badland_event_address = os.path.join(cwd,'assets/scenarios/Scenarios_Badzone_Events.csv')
    badland_df = pd.read_csv(badland_event_address, encoding='cp1252')
    badland_event_roll_ten = random.randint(1,6) * 10
    badland_event_roll_single = random.randint(1,6)
    badland_roll = badland_event_roll_ten+badland_event_roll_single
    badland_event = badland_df.loc[badland_df['roll'] == badland_roll]
    return badland_event['description'].values[0]

def get_scenario_df():
    scenarios_rel_address = 'assets/scenarios/Phase_1_Scenarios_Crew_select_first _roll.csv'    
    scenarios_df = pd.read_csv(os.path.join(cwd,scenarios_rel_address), encoding='cp1252')
    scenario_roll = random.randint(1,20)
    scenario = scenarios_df.loc[scenarios_df['roll'] == scenario_roll]
    return scenario

def get_traps(scenario):
    if scenario['has_traps'].values[0]:
        traps_address = 'assets/scenarios/Scenarios_Traps_roll.csv'
        traps_df = pd.read_csv(os.path.join(cwd, traps_address), encoding='cp1252')
        trap_roll = random.randint(1,8)
        selected_traps = traps_df.loc[traps_df['roll'] == trap_roll]
        trap_description = selected_traps['description'].values[0]
        second_trap_roll = random.randint(1,6)
        second_traps = selected_traps[f'option_{second_trap_roll}'].values[0]
        return f'{trap_description} {second_traps}'
    else: return

def get_loot_crate(scenario):
    if scenario['has_loot_crate'].values[0]:
        loot_address = 'assets/scenarios/Scenarios_Loot_crate_roll.csv'
        description = get_simple_df_content(loot_address, 6)
        return description
    else: return

def get_monster_roll(scenario):
    if scenario['has_monster_roll'].values[0]:
        loot_address = 'assets/scenarios/Scenarios_Monster_roll.csv'
        description = get_simple_df_content(loot_address, 6)
        return description
    else: return

def get_local_juves(scenario):
    if scenario['has_local_juves'].values[0]:
        text = get_participants_df_content('assets/scenarios/Scenarios_local_juves_roll.csv', 'Juves')
        return text
    else: return

def get_local_denizens(scenario):
    if scenario['has_local_denizens'].values[0]:
        text = get_participants_df_content('assets/scenarios/Scenarios_local_denizens_roll.csv', 'Local Denizens')
        return text
    else: return

def get_hive_dwellers(scenario):
    if scenario['has_hive_dwellers'].values[0]:
        text = get_participants_df_content('assets/scenarios/Scenarios_hive dwellers_roll.csv', 'Hive Dwellers')
        return text
    else: return

def get_convoy(scenario):
    if scenario['has_convoy'].values[0]:
        address = 'assets/scenarios/Scenarios_convoy_roll.csv'
        df = pd.read_csv(os.path.join(cwd, address), encoding='cp1252')
        defenders = random.randint(1, df["convoy_defenders_dice_size"].values[0]) + df["convoy_defenders_modifier"].values[0]
        carriages = random.randint(1, df["carriages_dice_size"].values[0]) + df["carriages_modifier"].values[0]
        return f"The convoy consists of {defenders} defenders and {carriages} carriages"
    else: return

def determine_attacker(first_gang, second_gang):
    roll1 = random.randint(1,40000)
    roll2 = random.randint(1,40000)
    if roll1 > roll2:
        return first_gang
    else: return second_gang

def get_crew_size(scenario, context):
    crew_dice = scenario[f'{context}_dice_crew_size'].values[0]
    crew_mod = scenario[f'{context}_crew_modifier'].values[0]
    if crew_dice == 0:
        return 0 + crew_mod
    else:
        return random.randint(1,crew_dice) + crew_mod

def get_embed(first_gang, second_gang, scenario, badland_scenario, traps, loot_crate, monster, local_juves, local_denizens, hive_dwellers, convoy, attacker, attacker_crew_method, defender_crew_method, attacker_crew_size, defender_crew_size, attacker_reinforcement, defender_reinforcement):
    embed = discord.Embed(
            title=f"{scenario['scenario_text'].values[0]}",
            description=f"Well, looks like we got ourself a good old scrap up between **{first_gang}** and **{second_gang}**. Turns out **{attacker}** is the attacker!",
            color=discord.Colour.dark_magenta(), # Pycord provides a class with default colors you can choose from
        )
    inline = False
    if badland_scenario:
        embed.add_field(name="Badland Scenario:", value=f"`{badland_scenario}`", inline=inline)
    if traps:
        embed.add_field(name="Traps", value=f"`{traps}`", inline=inline)
    if loot_crate:
        embed.add_field(name="Loot Crate(s):", value=f"`{loot_crate}`", inline=inline)
    if monster:
        embed.add_field(name="Monster:", value=f"`{monster}`", inline=inline)
    if local_juves:
        embed.add_field(name="Local Juves:", value=f"`{local_juves}`", inline=inline)
    if local_denizens:
        embed.add_field(name="Local Denizens:", value=f"`{local_denizens}`", inline=inline)
    if hive_dwellers:
        embed.add_field(name="Hive Dwellers:", value=f"`{hive_dwellers}`", inline=inline)
    if convoy:
        embed.add_field(name="Convoy Details:", value=f"`{convoy}`", inline=inline)
    attacker_reinforcement_text = ''
    if attacker_reinforcement:
        attacker_reinforcement_text = " Plus Reinforcements"
    defender_reinforcement_text = ''
    if defender_reinforcement:
        defender_reinforcement_text = " Plus Reinforcements"
    embed.add_field(name="Attacker Crew Details:", value=f"Attacker gets {attacker_crew_size} {attacker_crew_method} gangers!{attacker_reinforcement_text}", inline=inline)
    embed.add_field(name="Defender Crew Details:", value=f"Defender gets {defender_crew_size} {defender_crew_method} gangers!{defender_reinforcement_text}", inline=inline)
    embed.add_field(name="Gang URLS are as follows:", value=f"{first_gang} : {gangs.get(first_gang)}\r\n{second_gang}: {gangs.get(second_gang)}")
    return embed

def get_simple_df_content(address, dice):
    df = pd.read_csv(os.path.join(cwd, address), encoding='cp1252')
    dice_roll = random.randint(1,dice)
    selected = df.loc[df['roll'] == dice_roll]
    return selected['description'].values[0]


def get_participants_df_content(address, context):
        df = pd.read_csv(os.path.join(cwd, address), encoding='cp1252')
        roll = random.randint(1,df['dice_crew_size'].values[0]) + df['crew_modifier'].values[0]
        return f'A total of {roll} {context} turned up to play'