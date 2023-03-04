import discord
import wavelink
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from Addons.blacklist import blacklist_check
from Addons.loop import setLoop
from config import config


class loop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="loop", description="Repeats song.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(
        option=[ # param name
            Choice(name="🔂 Song", value="SONG"),
            Choice(name="🔁 Queue", value="QUEUE"),
            Choice(name="❌ Disabled", value="NONE")
        ]
    )
    async def loop(self, interaction: discord.Interaction, option: Choice[str]):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if option.value == "SONG":
                    setLoop(interaction.guild.id, "SONG")
                    embed = discord.Embed(title="Music", description='Looping one song 🔂✅', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                elif option.value == "QUEUE":
                    setLoop(interaction.guild.id, "QUEUE")
                    embed = discord.Embed(title="Music", description='Looping entire queue 🔁✅', colour=config.EMBED_COLOR)
                    embed.set_author(icon_url=interaction.user.display_avatar.url, name=interaction.user)
                    await interaction.followup.send(embed=embed)
                elif option.value == "NONE":
                    setLoop(interaction.guild.id, "NONE")
                    embed = discord.Embed(title="Music", description='Loop Disabled 🔁🔴!', colour=config.EMBED_COLOR)
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
    await bot.add_cog(loop(bot))