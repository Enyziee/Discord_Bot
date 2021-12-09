import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from urllib.parse import urlsplit

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_options)


def url_check(url):
    ps_url = urlsplit(url=url)

    if ps_url[1] == "www.youtube.com":
        if ps_url[3] != "":
            #return f"{ps_url[1]}{ps_url[2]}?{ps_url[3]}"
            return True

    elif ps_url[1] == "youtu.be":
        if ps_url[2] != "":
            #return f"{ps_url[1]}{ps_url[2]}"
            return True
            
    else:
        return None


class YDTLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def get_audio(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        song = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(song, **ffmpeg_options), data=data)


class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

# Entra no canal de voz
    @commands.command()
    async def join(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} você não está conectado a um canal de voz!")
            return
        
        channel = ctx.message.author.voice.channel
        await channel.connect()

# Desconecta do canal de voz
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Não estou conectado a um canal de voz!')
            return
        
        voice_client = ctx.voice_client
        await voice_client.disconnect()

# Começar a tocar a musica
    @commands.command(pass_context=True)
    async def play(self, ctx, url: str = None):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} Você não está conectado a um canal de voz!")
            return
        
        elif url_check(url) is None:
            await ctx.send("URL inválida!")
            return

        elif ctx.voice_client is None:
            channel = ctx.message.author.voice.channel
            self.player = await channel.connect()

        elif self.player.is_playing:
            await ctx.send(f'{ctx.message.author.mention} Ja esta tocando uma musica!')
            return

        async with ctx.typing():
            source = await YDTLSource.get_audio(url=url, loop=self.client.loop)
            self.player.play(source, after=lambda e: print(
                f'Player error {e}') if e else None)

        embed = discord.Embed(title="Reproduzindo agora:",
                              description=source.title)
        embed.set_thumbnail(url=source.data['thumbnail'])
        await ctx.send(embed=embed)

# Para a reprodução da música
    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} Você não está conectado a um canal de voz!")
            return
        if not self.player.is_playing:
            await ctx.send(f'{ctx.message.author.mention} Nao esta tocando musica tocar a muscia ')
            return

        self.player.stop()
        await ctx.send(f'{ctx.message.author.mention} Parando de tocar musica')


def setup(client):
    client.add_cog(Youtube(client))
