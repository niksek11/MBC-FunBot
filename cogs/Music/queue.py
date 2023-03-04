import time

import discord
import wavelink
from discord import app_commands
from discord.ext import commands

from Addons.blacklist import blacklist_check
from Addons.loop import getLoop
from config import config


class queue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="queue", description="Shows song list.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def queue(self, interaction: discord.Interaction):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if vc:
            if not vc.queue.is_empty:
                maxCount = 10*1; index = 0; start = False; totalTime = 0

                description = ""
                for song in vc.queue:
                    if index == maxCount-10: start = True
                    if not index == maxCount:
                        if start:
                            totalTime += song.length
                            dur = time.strftime('%H:%M:%S', time.gmtime(song.length))
                            description += f"\n**{index + 1}.** `[{dur}]` [{song.title}]({song.uri})"
                        index += 1

                if description:
                    
                    embed = discord.Embed(title=f"Songs:",description=f"Nr | Duration | Song Name\n{description}", colour=config.EMBED_COLOR); PageCount = len(vc.queue)/10
                    if "." in str(PageCount):
                        PageCount = int(str(PageCount).split(".")[0]) + 1

                    view = discord.ui.View()
                    view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏪", custom_id=f"queue_{interaction.user.id}_home"))
                    view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.success, emoji="◀", custom_id=f"queue_{interaction.user.id}_arrowLeft")) 
                    view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.danger, emoji="✖️", custom_id=f"queue_{interaction.user.id}_delete")) 
                    view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.success, emoji="▶", custom_id=f"queue_{interaction.user.id}_arrowRight"))
                    view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏩", custom_id=f"queue_{interaction.user.id}_end"))
                    try:
                        embed.set_author(icon_url=interaction.guild.icon.url, name=f"{interaction.guild.name}'s Queue")
                    except:
                        embed.set_author(name=f"{interaction.guild.name}'s Queue")
                    embed.set_footer(text=f"Page: 1/{PageCount}")
                    tt = time.strftime('%H:%M:%S', time.gmtime(totalTime))
                    await interaction.followup.send(content=f"▶️Now Playing: `{vc.source.title}` \n⏳Queue duration: `{tt}` \n📜Songs in queue: **{len(vc.queue)}** \n🔁Loop mode: `{getLoop(interaction.guild.id)}`", embed=embed, view=view)
                else:
                    error = discord.Embed(title="Music", description=f"No more pages! ❌", color=config.EMBED_COLOR)
                    error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=error)
            else:
                error = discord.Embed(title="Music", description=f"Queue is empty! ❌", color=config.EMBED_COLOR)
                error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                await interaction.followup.send(embed=error)
        else:
            error = discord.Embed(title="Music", description=f"No songs played right now! ❌", color=config.EMBED_COLOR)
            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
            await interaction.followup.send(embed=error, ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.get("custom_id"):
            if interaction.data["custom_id"].startswith("queue"):
                vc: wavelink.Player = interaction.guild.voice_client
                userID = int(interaction.data["custom_id"].split("_")[1]); type = interaction.data["custom_id"].split("_")[2]

                if userID == interaction.user.id:
                    if type == "delete":
                        view = discord.ui.View()

                        view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏪", disabled=True, custom_id=f"queue_{interaction.user.id}_home"))
                        view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.success, emoji="◀", disabled=True, custom_id=f"queue_{interaction.user.id}_arrowLeft")) 
                        view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.danger, emoji="✖️", disabled=True, custom_id=f"queue_{interaction.user.id}_delete")) 
                        view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.success, emoji="▶", disabled=True, custom_id=f"queue_{interaction.user.id}_arrowRight"))
                        view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏩", disabled=True, custom_id=f"queue_{interaction.user.id}_end"))
                            
                        return await interaction.response.edit_message(embed=interaction.message.embeds[0], view=view)
                    if vc:
                        Page = int(interaction.message.embeds[0].footer.text.replace("Page: ", "").split("/")[0])
                        if type == "arrowLeft":

                            Page -= 1

                        elif type == "arrowRight":

                            Page += 1

                        elif type == "home":
                            Page = 1

                        if not vc.queue.is_empty:
                            PageCount = len(vc.queue)/10
                            if "." in str(PageCount):
                                PageCount = int(str(PageCount).split(".")[0]) + 1
                            if type == "end":
                                Page = PageCount

                            maxCount = 10*Page; index = 0; start = False; totalTime = 0

                            description = ""
                            for song in vc.queue:
                                if index == maxCount-10: start = True
                                if not index == maxCount:
                                    if start:
                                        totalTime += song.length
                                        dur = time.strftime('%H:%M:%S', time.gmtime(song.length))
                                        description += f"\n**{index + 1}.** `[{dur}]` [{song.title}]({song.uri})"
                                    index += 1

                            if description:
                                
                                embed = discord.Embed(title=f"Songs:", description=f"Nr | Duration | Song Name\n{description}", colour=config.EMBED_COLOR)

                                try:
                                    embed.set_author(icon_url=interaction.guild.icon.url, name=f"{interaction.guild.name}'s Queue")
                                except:
                                    embed.set_author(name=f"{interaction.guild.name} Queue's")
                                embed.set_footer(text=f"Page: {Page}/{PageCount}")
                                tt = time.strftime('%H:%M:%S', time.gmtime(totalTime))
                                await interaction.response.edit_message(content=f"▶️Now Playing: `{vc.source.title}` \n⏳Queue duration: `{tt}` \n📜Songs in queue: **{len(vc.queue)}** \n🔁Loop mode: `{getLoop(interaction.guild.id)}`", embed=embed)
                            else:
                                error = discord.Embed(title="Music", description=f"No more pages! ❌", color=config.EMBED_COLOR)
                                error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                                await interaction.channel.send(embed=error)
                        else:
                            error = discord.Embed(title="Music", description=f"Queue is empty! ❌", color=config.EMBED_COLOR)
                            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                            await interaction.channel.send(embed=error)    
                    else:
                        error = discord.Embed(title="Music", description='No music is being played right now! ❌', colour=config.EMBED_COLOR)
                        error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                        await interaction.channel.send(embed=error)
                else:
                    error = discord.Embed(title="Music", description='This is not your panel! ❌', colour=config.EMBED_COLOR)
                    error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.channel.send(embed=error)


async def setup(bot: commands.Bot):
    await bot.add_cog(queue(bot))