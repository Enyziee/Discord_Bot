import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

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


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} você não está conectado a um canal de voz!")
            return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Não estou conectado a um canal de voz!')
            return

        voice_client = ctx.voice_client
        await voice_client.disconnect()

    @commands.command(pass_context=True)
    async def play(self, ctx, url: str = None):
        if ctx.message.author.voice is None:
            await ctx.send(f"{ctx.message.author.mention} Você não está conectado a um canal de voz!")
            return

        if not url:
            await ctx.send(',k')
            return

        channel = ctx.message.author.voice.channel
        player = await channel.connect()

        async with ctx.typing():
            source = await YDTLSource.get_audio(url=url, loop=self.client.loop)
            player.play(source, after=lambda e: print(
                f'Player error {e}') if e else None)

        embed = discord.Embed(title="Reproduzindo agora:",
                              description=source.title)
        embed.set_thumbnail(url=source.data['thumbnail'])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
