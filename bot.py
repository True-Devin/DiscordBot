import asyncio
import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv

import eloSearchBar
from EloSearch import main
from eloSearchBar import main2

load_dotenv()
user_input = ""

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(status_task())


@bot.command()
async def hello(ctx):
    await ctx.reply('Hello!')


@bot.command()
async def elo(ctx, search):
    search_result = main2(search)
    if search_result is None:
        print("No Player found")
        await ctx.send("No Player found")
    else:
        clean_result, max_chr_alert = eloSearchBar.paste(search_result)
        if max_chr_alert:
            embed_var = discord.Embed(title=f"Search Results for: __{search}__", color=discord.Color.red())
        else:
            embed_var = discord.Embed(title=f"Search Results for: __{search}__", color=discord.Color.green())
        embed_var.add_field(name="Name      Character       Elo     Games Played",
                            value=f"{clean_result}", inline=False)
        await ctx.send(embed=embed_var)


@bot.command()
async def elo2(ctx, character, search):
    search_result = main(character, search)
    if search_result is None:
        print("No Player found")
        await ctx.send("No Player found")
    else:
        embed_var = discord.Embed(title=f"{search_result[1]}'s ELO", color=0xa0a0a0)
        embed_var.add_field(name="Rank", value=f"#{search_result[0]}", inline=False)
        embed_var.add_field(name="Name", value=search_result[1], inline=False)
        embed_var.add_field(name="Elo", value=search_result[2], inline=False)
        embed_var.add_field(name="Games Played", value=search_result[3], inline=False)
        await ctx.send(embed=embed_var)


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('Guilty Gear: Strive'))
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Game('6P Simulator'))
        await asyncio.sleep(60)


bot.run(getenv('TOKEN'))
