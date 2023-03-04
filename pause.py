import wavelink
import discord
from discord import app_commands
from discord.ext import commands
from config import config
from Addons.blacklist import blacklist_check

class pause(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="pause", description="Pauses played song.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def pause(self, interaction: discord.Interaction):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if vc.pause:
                    embed = discord.Embed(title="Music", description='Already paused ❌', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                else:
                    await vc.set_pause(True)
                    embed = discord.Embed(title="Music", description='Playback paused ⏸️', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
            else:
                error = discord.Embed(title="Music", description='No music is being played right now! ❌', colour=config.EMBED_COLOR)
                error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                await interaction.followup.send(embed=error, ephemeral=True)
        else:
            error = discord.Embed(title="Music", description=f"You need to be in voice channel! ❌", color=config.EMBED_COLOR)
            error.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
            await interaction.followup.send(embed=error, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(pause(bot))