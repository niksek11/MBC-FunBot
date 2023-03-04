import wavelink
import discord
from discord import app_commands
from discord.ext import commands
from config import config
import re
from Addons.blacklist import blacklist_check

TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"

class seek(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="seek", description="Seeks current song to given position (60s or 2:30 or 1:05).")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def seek(self, interaction: discord.Interaction, position: str):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if not vc.is_playing():
                    error = discord.Embed(title="Music", description='Nothing is being played right now! ❌', colour=config.EMBED_COLOR)
                    error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=error)
                    return

                if not (match := re.match(TIME_REGEX, position)):
                    error = discord.Embed(title="Music", description='Invalid time type!  Try something like this: 60s or 2:30 or 1:05 ❌', colour=config.EMBED_COLOR)
                    error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=error)
                    return

                if match.group(3):
                    secs = (int(match.group(1)) * 60) + (int(match.group(3)))
                else:
                    secs = int(match.group(1))

                await vc.seek(secs * 1000)
                error = discord.Embed(title="Music", description=f'Seeked current song to position: `{position}`! ⏭️', colour=config.EMBED_COLOR)
                error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                await interaction.followup.send(embed=error)
            else:
                error = discord.Embed(title="Music", description='No music is being played right now! ❌', colour=config.EMBED_COLOR)
                error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                await interaction.followup.send(embed=error, ephemeral=True)
        else:
            error = discord.Embed(title="Music", description=f"You need to be in voice channel! ❌", color=config.EMBED_COLOR)
            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
            await interaction.followup.send(embed=error, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(seek(bot))


