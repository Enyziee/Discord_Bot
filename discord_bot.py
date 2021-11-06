from tk import token
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='we!')


@client.event
async def on_ready():
    print("O Bot está pronto")


@client.command
async def play(ctx):
    channel = ctx.message.author.voice.channel
    print(channel)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message)
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run(token)
