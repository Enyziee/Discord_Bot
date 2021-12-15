import os
import json
from discord.flags import Intents
from discord.ext import commands
from dotenv import load_dotenv

# Token do bot
load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")

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


# Inicializa o objeto com o Discord Bot
client = commands.Bot(
    command_prefix=get_prefix,
    intents=Intents.default()
)


# Inicializa as COGS
def init_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith("cog.py"):
            client.load_extension(f"cogs.{cog[:-3]}")
            print(f"{cog[:-3].capitalize()} carregada.")


# Desativa as COGS
def deact_cogs():
    for cog in os.listdir("cogs/"):
        if cog.endswith("cog.py"):
            client.unload_extension(f"cogs.{cog[:-3]}")
            print(f"{cog[:-3].capitalize()} descarregada.")


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


@client.event
async def on_ready():
    print("Iniciando cogs...")
    init_cogs()
    print("O Bot está pronto!")


@client.command()
async def _restart(ctx):
    deact_cogs()
    init_cogs()
    await ctx.send("Cog restarted")


if __name__ == "__main__":
    client.run(TOKEN)
