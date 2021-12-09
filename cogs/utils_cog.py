from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client
        
#funcao do comando clear(delata mensagens)
    @commands.command()
    async def clear(self, ctx, limit=1):
        deleted = await ctx.channel.purge(limit=limit+1)

        if len(deleted) == 0:
            await ctx.send('Nenhuma mensagem apagada!')
        elif len(deleted) == 1:
            await ctx.send('1 mensagem apagada!')
        else:
            await ctx.send(f'{len(deleted)} mensagens apagadas!')  
 
 #funcao memes, retorna        
    @commands.command()
    async def sim(self, ctx):
        await ctx.send("nao") 

    @commands.command()
    async def nao(self, ctx):
        await ctx.send("sim")


def setup(client):
    client.add_cog(Utils(client))
