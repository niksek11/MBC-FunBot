import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
<<<<<<< HEAD

=======
>>>>>>> 26672cc244ea3b22cd3324d7a9df2063a5922054

class MyBot(commands.Bot):
    async def setup_hook(self):
        for folder in os.listdir('./cogs'):
            for file in os.listdir(f'./cogs/{folder}'):
                if file.endswith('.py'):
                    await self.load_extension(f'cogs.{folder}.{file[:-3]}')
                    bot.extensions_list += f"{folder}.{file[:-3]}, "


intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.guilds = True

bot = MyBot(command_prefix=".", intents=intents)

bot.extensions_list = ""
bot.remove_command('help')

extensionsArray = bot.extensions_list.split(",")

<<<<<<< HEAD

# Load message in console :)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='/help', url='https://twitch.tv/Insym'))

=======
#Load message in console :)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='/help', url='https://twitch.tv/Insym'))
    
>>>>>>> 26672cc244ea3b22cd3324d7a9df2063a5922054
    print("[-] Starting BOT... Please Wait 🟡")
    print(f"[-] Bot Extensions 📂 ({len(extensionsArray)})")
    print(bot.extensions_list)
    print("[-] Logged in as {0.user} 🤖".format(bot))
    print("[-] Startup Complete! 🟢")


@bot.event
async def on_guild_join(guild):
    print(f"➕ NEW GUILD: {guild.name} ({guild.id})")
<<<<<<< HEAD


=======
    
>>>>>>> 26672cc244ea3b22cd3324d7a9df2063a5922054
@bot.event
async def on_guild_remove(guild):
    print(f"➖ REMOVED GUILD: {guild.name} ({guild.id})")

<<<<<<< HEAD

bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
=======
bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
>>>>>>> 26672cc244ea3b22cd3324d7a9df2063a5922054
