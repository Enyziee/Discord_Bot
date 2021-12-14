import os
from dotenv import load_dotenv
from discord.ext import commands
#libs utilizadas


client = commands.Bot(command_prefix=".", ) 
#prefixo utilizado para chamar o bot(.)


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
#token do bot


def init_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            client.load_extension(f"cogs.{cog[:-3]}")

def deact_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            client.unload_extension(f"cogs.{cog[:-3]}")
#funcoes para iniciar e desligar os cogs


@client.event
async def on_ready():
    print("Iniciando cogs...")
    init_cogs()
    print("O Bot está pronto!")
    
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
    deact_cogs()
    init_cogs()
    await ctx.send("Cog restarted")
#funcoes para avisar quando o bot iniciar, as cogs estiverem ligadas, desligadas, ou quando forem reiniciadas respectivamente


client.run(BOT_TOKEN)
