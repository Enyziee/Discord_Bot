import discord
from discord.ext import commands
from discord.ext.commands.core import command

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f" we have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message)
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run("ODk3OTQ5MDYyOTc5MDI3MDA0.YWdGOw.HGH7JUrna0BjZ4V-XJIxuewFPGY")
