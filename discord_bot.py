import os
import json

from discord.flags import Intents
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound
import discord

from my_logging import log

TOKEN = os.getenv('TOKEN')

TOKEN = "OTE5MDgzNzMwMzk4NzYxMDMw.GH64qJ.iCP9FLvFc6bYmPSbJ576_KDqJzPKvAU98fPHUA"

# Arquivo onde será salvo o prefixo de de cada servidor
PREFIX_FILE = "guilds_prefix.json"
DEFAULT_PREFIX = "!"

if PREFIX_FILE not in os.listdir():
    with open(PREFIX_FILE, "w") as file:
        json.dump(dict(), file, indent=4)


# Retorna o prefixo designado para cada servidor
def get_prefix(client, message):
    with open(PREFIX_FILE, "r") as file:
        prefixes = json.load(file)

        if not prefixes.values():
            return DEFAULT_PREFIX

    return prefixes[str(message.guild.id)]

activity = discord.Game(name="Prefix = !")

# Inicializa o objeto com o Discord Bot
client = commands.Bot(
    command_prefix=DEFAULT_PREFIX,
    intents=Intents.default(),
    activity=activity,
)

# bot = commands.Bot(command_prefix="!", activity=activity, status=discord.Status.idle)


# Inicializa as COGS
def init_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith("cog.py"):
            try:
                client.load_extension(f"cogs.{cog[:-3]}")
            except Exception as e:
                print(e)


# Desativa as COGS
def deact_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith("cog.py"):
            try:
                client.unload_extension(f"cogs.{cog[:-3]}")
            except Exception as e:
                print(e)


# Adiciona o servidor no PREFIX_FILE
@client.event
async def on_guild_join(guild):
    with open(PREFIX_FILE, "r",) as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = DEFAULT_PREFIX

    with open(PREFIX_FILE, "w",) as file:
        json.dump(prefixes, file, indent=4)


# Remove o servidor do PREFIX_FILE
@client.event
async def on_guild_remove(guild):
    with open(PREFIX_FILE, 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open(PREFIX_FILE, 'w') as file:
        json.dump(prefixes, file, indent=4)

@client.command()
async def guild_join(ctx):
    with open(PREFIX_FILE, "r",) as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = DEFAULT_PREFIX

    with open(PREFIX_FILE, "w",) as file:
        json.dump(prefixes, file, indent=4)


@client.command()
async def guild_remove(ctx):
    with open(PREFIX_FILE, 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(ctx.guild.id))

    with open(PREFIX_FILE, 'w') as file:
        json.dump(prefixes, file, indent=4)



# Reinicia as cogs
@client.command(hidden=True)
async def restart(ctx):
    deact_cogs()
    init_cogs()
    log("Cogs reiniciadas")


@client.event
async def on_ready():
    log("Iniciando cogs...")
    init_cogs()
    log("O Bot está pronto!")


@client.event
async def on_command_error(ctx, exception, /):
    if isinstance(exception, CommandNotFound):
        log(msg=exception, user=(f'{ctx.author.name}#{ctx.author.discriminator}'))


@client.event
async def on_error(ctx, exception):
    log(msg=exception, user=(f'{ctx.author.name}#{ctx.author.discriminator}'))


if __name__ == "__main__":
    client.run(TOKEN)
