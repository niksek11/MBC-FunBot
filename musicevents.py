import wavelink
from discord.ext import commands

from Addons.loop import getLoop


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="127.0.0.1", port=2333, password="password")
        
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Wavelink: node <{node.identifier}> is ready | Lavalink connected! 🟢")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if reason == "STOPPED":
            if not player.queue.is_empty:
                new = await player.queue.get_wait()
                await player.play(new)
            else:
                await player.stop()
        elif reason == "FINISHED":
            if getLoop(player.guild.id) == "NONE":
                new = await player.queue.get_wait()
                await player.play(new)
            elif getLoop(player.guild.id) == "SONG":
                await player.play(track)
            elif getLoop(player.guild.id) == "QUEUE":
                if player.queue.is_empty and not player.is_playing():
                    await player.play(track)
                else:
                    await player.play(await player.queue.get_wait())
                    await player.queue.put_wait(track)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))