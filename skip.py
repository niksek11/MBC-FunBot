import wavelink
import discord
from discord import app_commands
from discord.ext import commands
from config import config
from Addons.blacklist import blacklist_check

class skip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="skip", description="Skips song.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def skip(self, interaction: discord.Interaction):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if not vc.queue.is_empty:
                    embed=discord.Embed(description=f"Skipped: [{vc.source.title}]({vc.source.uri}) ⏭️",colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                    await vc.stop()
                else:
                    error = discord.Embed(title="Music", description=f"No next song! ❌", colour=config.EMBED_COLOR, timestamp=discord.utils.utcnow())
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
    await bot.add_cog(skip(bot))