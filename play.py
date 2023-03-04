import time

import discord
import wavelink
from discord import app_commands
from discord.ext import commands
from discord.ui import View

from Addons.blacklist import blacklist_check
from Addons.loop import setLoop
from config import config


class play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play", description="Plays songs.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def play(self, interaction: discord.Interaction, songname: str):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        if interaction.user.voice:
            await interaction.followup.send(embed=discord.Embed(description=f"Searching song: `{songname}` 🎶", color=config.EMBED_COLOR))

            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
                setLoop(interaction.guild.id, "NONE")
            else:
                vc: wavelink.Player = interaction.guild.voice_client

            if songname.startswith("https://"):
                if "playlist?" in songname:
                    try:
                        playlist = await wavelink.YouTubePlaylist.search(query=songname)
                        for track in playlist.tracks:
                            track.requester = interaction.user
                            await vc.queue.put_wait(track)
                        if not vc.is_playing():
                            track = await vc.queue.get_wait()
                            await vc.play(track)
                        await interaction.edit_original_response(embed=discord.Embed(title="Music", description=f"Added to queue `{len(playlist.tracks)}` song from playlist `{playlist.name}`", color=config.EMBED_COLOR))
                    except:
                        await interaction.edit_original_response(content=f"Error: Song not found")
                else:
                    try:
                        track = await vc.node.get_tracks(query=songname, cls=wavelink.Track); track[0].requester = interaction.user
                    except:
                        await interaction.edit_original_response(content=f"Error: Ups! coś się spierdoliło! ale nawet sam autor niewie co LOL ale chyba masz zły link")

                    if not len(track) == 0:
                        if vc.queue.is_empty and not vc.is_playing():
                            await vc.play(track[0])
                        else:
                            await vc.queue.put_wait(track[0])
                        await interaction.edit_original_response(embed=discord.Embed(title="Music", description=f"Added to queue: [{track[0].title}]({track[0].uri})", color=config.EMBED_COLOR))
                    else:
                        await interaction.edit_original_response(content=f"Error: Song not found")
            else:
                track = await wavelink.YouTubeTrack.search(songname); index = 0; values = []

                if len(track) == 1:
                    if vc.queue.is_empty and not vc.is_playing():
                        await vc.play(track[0])
                    else:
                        await vc.queue.put_wait(track[0])
                    return await interaction.edit_original_response(embed=discord.Embed(title="Music", description=f"Added to queue: [{track[0].title}]({track[0].uri})", color=config.EMBED_COLOR))
                elif len(track) == 0:
                    return await interaction.edit_original_response(content=f"Error: Song not found")
                description = ""
                for song in track:
                    if not index == 5:
                        position = time.strftime('%H:%M:%S', time.gmtime(song.length))
                        description += f"**{index + 1}.** `[{position}]` {song.title}\n"
                        values.append(discord.SelectOption(label=f"{index + 1}. [{position}] {song.title[:60-3] + (song.title[60-3:], '...')[len(song.title) > 60]}", value=song.uri))
                        index += 1

                class Dropdown(discord.ui.Select):
                    def __init__(self):
                        options = values

                        super().__init__(placeholder='Select one song please!', custom_id=f"songMenu_{interaction.user.id}", options=options)

                    async def callback(self, interaction: discord.Interaction):
                        userID = int(interaction.data["custom_id"].split("_")[1])
                        if interaction.user.id == userID:
                            track = await vc.node.get_tracks(query=self.values[0], cls=wavelink.Track); track[0].requester = interaction.user

                            if vc.queue.is_empty and not vc.is_playing():
                                await vc.play(track[0])
                            else:
                                await vc.queue.put_wait(track[0])
                            
                            await interaction.response.edit_message(embed=discord.Embed(title="Music", description=f"Added to queue: [{track[0].title}]({track[0].uri})", color=config.EMBED_COLOR), view=View())
                        else:
                            error = discord.Embed(title="Music", description='This is not your panel! ❌', colour=config.EMBED_COLOR)
                            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                            await interaction.followup.send(embed=error)

                class DropdownView(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.add_item(Dropdown())

                view = DropdownView()

                await interaction.edit_original_response(embed=discord.Embed(title="Search result:", description=description, color=config.EMBED_COLOR), view=view)
        else:
            error = discord.Embed(title="Music", description=f"You need to be in voice channel! ❌", color=config.EMBED_COLOR)
            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
            await interaction.followup.send(embed=error)

async def setup(bot: commands.Bot):
    await bot.add_cog(play(bot))