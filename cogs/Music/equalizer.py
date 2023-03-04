import wavelink
import discord
from discord import app_commands
from discord.ext import commands
from config import config
from discord.app_commands import Choice
from Addons.blacklist import blacklist_check

class equalizer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="equalizer", description="Changes music equalizer.")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(
        option=[ # param name
            Choice(name="1️⃣ Flat", value="FLAT"),
            Choice(name="2️⃣ Boost", value="BOOST"),
            Choice(name="3️⃣ Metal", value="METAL"),
            Choice(name="4️⃣ Piano", value="PIANO")
        ]
    )
    async def equalizer(self, interaction: discord.Interaction, option: Choice[str]):
        if await blacklist_check(self.bot, interaction): return  # blacklist check
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if vc:
                if option.value == "FLAT":
                    preset = wavelink.Equalizer.flat()
                    wpreset = "flat"
                elif option.value == "BOOST":
                    preset = wavelink.Equalizer.boost()
                    wpreset = "boost"
                elif option.value == "METAL":
                    preset = wavelink.Equalizer.metal()
                    wpreset = "metal"
                elif option.value == "PIANO":
                    preset = wavelink.Equalizer.piano()
                    wpreset = "piano"
                
                    
                await vc.set_filter(wavelink.Filter(equalizer=preset))
                embed = discord.Embed(title="Music", description=f'Equaliser adjusted to the `{wpreset}` preset. ✅', colour=config.EMBED_COLOR)
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
    await bot.add_cog(equalizer(bot))


