import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

client = commands.Bot(command_prefix='we!', )
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

@client.event
async def on_ready():
    print("O Bot está pronto")


@task.loop(seconds=5)


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def join(ctx):
    if not ctx.message.author.voice.channel:
        await ctx.send(f"Você não está conectado a um canal de voz {ctx.message.author.name}")
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


@client.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@client.command()
async def sendmsg(ctx):
    await ctx.send("alskdhalsdhlasd")

client.run(BOT_TOKEN)
