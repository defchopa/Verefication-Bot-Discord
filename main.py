import disnake
from disnake.ext import commands,tasks
import os
import asyncio
import config
from config import *

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())
bot.remove_command('help')

@bot.command()
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')

@bot.command
async def on_ready():
    print(config['print'])

@bot.command()
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')

for filename in os.listdir(".\cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config["token"])