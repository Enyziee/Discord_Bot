import os
from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix='we!', )
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
    print("O Bot está pronto")
    client.load_extension('cogs.music_cog')
    client.load_extension('cogs.utils_cog')


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def load(ctx):
    client.load_extension(f'cogs.music_cog')
    await ctx.send("Cog loaded")


@client.command()
async def unload(ctx):
    client.unload_extension(f'cogs.music_cog')
    await ctx.send("Cog unloaded")


@client.command()
async def restart(ctx):
    client.unload_extension(f'cogs.music_cog')
    client.load_extension(f'cogs.music_cog')
    await ctx.send("Cog restarted")


client.run(BOT_TOKEN)
