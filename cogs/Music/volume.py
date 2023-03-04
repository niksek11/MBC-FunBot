import wavelink
import discord
from discord import app_commands
from discord.ext import commands
from config import config
from Addons.blacklist import blacklist_check

class volume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="volume", description="Changes music volume.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def volume(self, interaction: discord.Interaction, vol: int):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if vol < 0:
                    embed = discord.Embed(title="Music", description='The volume must be 0% or above ❌', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                    return
                if vol > 150:
                    embed = discord.Embed(title="Music", description='The volume must be 150% or  below ❌', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                    return
                await vc.set_volume(vol)
                embed = discord.Embed(title="Music", description=f"Volume set to {vol:,}% ✅", colour=config.EMBED_COLOR)
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
    await bot.add_cog(volume(bot))


