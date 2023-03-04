import time

import discord
import wavelink
from discord import app_commands
from discord.ext import commands, tasks

from Addons.blacklist import blacklist_check
from Addons.loop import getLoop
from config import config


class nowplaying(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    server_map = {}  

    @tasks.loop(seconds=5)
    async def npu(self):
        try:
            for guild in self.bot.guilds:
                vc: wavelink.Player = guild.voice_client
                if vc:
                    guild_id = guild.id
                    try:
                        message_object = self.server_map.get(guild_id)
                    except:
                        return
                    try:
                        msg = message_object
                    except:
                        return
                    try:
                        if vc.source:
                            if vc.is_playing():
                                poz = vc.position
                                dur = vc.source.length
                                per = round((poz / dur) * 100)
                                b = round(per / 5)
                                g = b
                                pbar = ((g - 1) * '▬' + ':radio_button:' + (20 - b) * '▬')
                                embed = discord.Embed(title="Now Playing", description=f"[{vc.source.title}]({vc.source.uri}) \nAuthor: {vc.source.author}", color=config.EMBED_COLOR)
                                position = time.strftime('%H:%M:%S', time.gmtime(vc.position))
                                length = time.strftime('%H:%M:%S', time.gmtime(vc.source.length))
                                #volume
                                if vc.volume > 99:
                                    vemoji = "🔊"
                                if 100 > vc.volume > 50:
                                    vemoji = "🔉"
                                if 0 < vc.volume < 51:
                                    vemoji = "🔈"
                                if vc.volume == 0:
                                    vemoji = "🔇"
                                embed.add_field(name="Progress", value=f"▶️{pbar}`[{position}/{length}]` {vemoji}{vc.volume}%\n🔁Loop Mode: {getLoop(guild.id)}", inline=False)
                                try:
                                    await msg.edit(embed=embed)
                                except:
                                    return
                        else:
                            embed = discord.Embed(title="Now Playing", description=f"Nothing is being played right now", color=config.EMBED_COLOR)
                            #volume
                            if vc.volume > 99:
                                vemoji = "🔊"
                            if 100 > vc.volume > 50:
                                vemoji = "🔉"
                            if 0 < vc.volume < 51:
                                vemoji = "🔈"
                            if vc.volume == 0:
                                vemoji = "🔇"
                            embed.add_field(name="Progress", value=f"⏸️🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬`[00:00:00/00:00:00]` {vemoji}{vc.volume}%\n🔁Loop Mode: {getLoop(guild.id)}", inline=False)
                            try:
                                await msg.edit(embed=embed)
                            except:
                                return
                    except:
                        return
        except:
            return

    @commands.Cog.listener()
    async def on_ready(self):
        await self.npu.start()

    @app_commands.command(name="nowplaying", description="Shows now played song.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def now_playing(self, interaction: discord.Interaction):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if vc:
            if vc.source:
                
                poz = vc.position
                dur = vc.source.length
                per = round((poz / dur) * 100)
                b = round(per / 5)
                g = b
                pbar = ((g - 1) * '▬' + ':radio_button:' + (19 - b) * '▬')

                embed = discord.Embed(title="Now Playing", description=f"[{vc.source.title}]({vc.source.uri}) \nAuthor: {vc.source.author}", color=config.EMBED_COLOR)
                position = time.strftime('%H:%M:%S', time.gmtime(vc.position))
                length = time.strftime('%H:%M:%S', time.gmtime(vc.source.length))

                #volume
                if vc.volume > int('99'):
                    vemoji = "🔊"
                if int('100') > vc.volume > int('50'):
                    vemoji = "🔉"
                if int('0') < vc.volume < int('51'):
                    vemoji = "🔈"
                if vc.volume == int('0'):
                    vemoji = "🔇"

                embed.add_field(name="Progress", value=f"▶️{pbar}`[{position}/{length}]` {vemoji}{vc.volume}%\n🔁Loop Mode: {getLoop(interaction.guild.id)}",inline=False)
                await interaction.followup.send(embed=embed)
                message_object = await interaction.original_response()
                guild_id = interaction.guild.id
                self.server_map[guild_id] = message_object
                
            else:
                embed = discord.Embed(title="Music", description='No music is being played right now! ❌', colour=config.EMBED_COLOR)
                embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                await interaction.followup.send(embed=embed, ephemeral=True)
                
        else:
            embed = discord.Embed(title="Music", description='No music is being played right now! ❌', colour=config.EMBED_COLOR)
            embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(nowplaying(bot))
