import os
from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix="!", )
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def init_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            client.load_extension(f"cogs.{cog[:-3]}")

def deact_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            client.unload_extension(f"cogs.{cog[:-3]}")

@client.event
async def on_ready():
    print("Iniciando cogs...")
    init_cogs()
    print("O Bot está pronto!")
    


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def load(ctx):
    init_cogs()
    await ctx.send("Cog loaded")


@client.command()
async def unload(ctx):
    deact_cogs()
    await ctx.send("Cog unloaded")


@client.command()
async def restart(ctx):
    init_cogs()
    deact_cogs()
    await ctx.send("Cog restarted")


client.run(BOT_TOKEN)
