import discord
from discord.ext import commands

import asyncio
from functools import partial
from async_timeout import timeout
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
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


# Classes para erros personalizados 

class InvalidVoiceChannel(commands.CommandError):
    pass

class VoiceConnectionError(commands.CommandError):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')


    # Cria o objeto de stream do video requisitado
    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        try:
            to_run = partial(ytdl.extract_info, url=search, download=download)
            data = await loop.run_in_executor(None, to_run)
        
        except DownloadError as e:
            return e

        # Pega o primeiro item de uma playlist
        if 'entries' in data:
            data = data['entries'][0]

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=ctx.author)
    

# Classe que cria um player de áudio dedicado para cada servidor
class MusicPlayer:

    __slots__ = ('bot', '_guild', '_channel', '_cog',
                 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx) -> None:
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()

            except asyncio.TimeoutError as e:
                return self.destroy(self._guild)

            self._guild.voice_client.play(
                source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

            self.np = await self._channel.send(f"**Reproduzindo agora:** `{source.title}`")

            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


# Classe com os comandos
class Music(commands.Cog):

    __slots__ = ("client", "players")

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.players = {}

    
    # Pega um player já existente ou cria um novo
    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player    


    # Destrói o player do servidor
    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    
    # Comando para colocar o bot em um canal de voz
    @commands.command(hidden=True, aliases=["join"], help="Entra em um canal de voz")
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel

            except AttributeError:
                return await ctx.send(f"Você não está conectado a um canal de voz!")
                
        vc = ctx.voice_client
        
        if vc:
            if vc.channel.id == channel.id:
                return

            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Conectado no canal: **{channel}**', delete_after=15)
    

    # Começar a tocar a música
    @commands.command(help="Reproduz um video do youtube")
    async def play(self, ctx, *search):    

        search = " ".join(search)
        player = self.get_player(ctx)
        source = await YTDLSource.create_source(ctx, search, loop=self.client.loop)

        if isinstance(source, DownloadError):
            return await ctx.send(f"URL inválida:", delete_after=15)

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect)        

        await player.queue.put(source)


    @commands.command(aliases=["next"], help="Avança para a próxima música da fila")
    async def skip(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"Não estou tocando nada no momento!", delete_after=15)
    
        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send("Indo para próxima musica!")
        
    @commands.command(help="Para a reprodução e limpa a fila de musicas")
    async def stop(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"Não estou tocando nada no momento!", delete_after=15)

        await self.cleanup(ctx.guild)


def setup(client):
    client.add_cog(Music(client))