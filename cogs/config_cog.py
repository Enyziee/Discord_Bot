import json
from discord.ext import commands
from discord.ext.commands.core import has_permissions

# Nome do arquivo dos prefixos 
from discord_bot import PREFIX_FILE

class Config(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    @commands.command(pass_context=True, help="Altera o prefixo do bot")
    @has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        with open(PREFIX_FILE, "r") as file:
            prefixes = json.load(file)

        prefixes[(str(ctx.guild.id))] = prefix

        with open(PREFIX_FILE, "w") as file:
            json.dump(prefixes, file, indent=4)

        await ctx.send(f"Novo prefixo é {prefix}")


def setup(client):
    client.add_cog(Config(client))