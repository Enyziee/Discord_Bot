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
    'quiet': True,
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
            return True

    elif ps_url[1] == "youtu.be":
        if ps_url[2] != "":
            return True

    else:
        return None


class Queue():
    def __init__(self):
        self.queue = []

    def add(self, source):
        self.queue.append(source)

    def skip(self, player):
        song = self.queue[0]
        self.queue.pop(0)
        player.play(song)

    def list(self):
        return self.queue


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.6):
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
        self.queue = []


# Começar a tocar a musica

    @commands.command()
    async def play(self, ctx, url: str = None):
        if ctx.message.author.voice is None:
            await ctx.send(f"Você não está conectado a um canal de voz!")
            return

        elif url_check(url) is None:
            await ctx.send("URL inválida!")
            return

        elif ctx.voice_client is None:
            channel = ctx.message.author.voice.channel
            self.player = await channel.connect()

        # elif self.player.is_playing:
        #     await ctx.send(f'Já esta tocando uma musica!')
        #     return


        async with ctx.typing():
            source = await YTDLSource.get_audio(url, loop=self.client.loop)

            if len(self.queue) == 0:

                self.start_playing(source)
                await ctx.send(f"tocando: {self.player}")

            else:
                self.queue.append(source)
                await ctx.send("Na fila: {source.title}")


        embed = discord.Embed(title="Reproduzindo agora:",
                              description=source.title)
        embed.set_thumbnail(url=source.data['thumbnail'])
        await ctx.send(embed=embed)

    def start_playing(self, source):
        self.queue.insert(0, source)
        i = 0
        while i < len(self.queue):
            self.player.play(self.queue[i], after=lambda e: print(
                'Player error: %s' % e) if e else None)
            
            i += 1

            
# Desconecta do canal de voz

    @commands.command()
    async def leave(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"Você não está conectado a um canal de voz!")
            return

        elif ctx.voice_client is None:
            await ctx.send("Não estou conectado a um canal de voz!")
            return

        await ctx.voice_client.disconnect()


    # @commands.command()
    # async def add_queue(self, ctx, url: str):
    #     source = await YTDLSource.get_audio(url=url, loop=self.client.loop)
    #     self.queue.add(source)

    # @commands.command()
    # async def queue(self, ctx):
    #     for item in self.queue.list():
    #         await ctx.send(f"{item.title}")


# Parar a reprodução da música

    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"Você não está conectado a um canal de voz!")
            return

        elif self.player is None:
            await ctx.send("Não estou conectado a um canal de voz!")
            return

        elif not self.player.is_playing:
            await ctx.send(f"Não estou tocando nada!")
            return

        self.player.stop()
        await ctx.send(f'Parando...')


def setup(client):
    client.add_cog(Youtube(client))
