import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
cwd = Path(__file__).parents[0]
cwd = str(cwd)

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

#load message
@bot.event
async def on_ready():
    print("[-] Starting BOT... Please Wait 🟡")
    await bot.change_presence(activity=discord.Streaming(name='/help', url='https://twitch.tv/Insym'))


    print(f"[-] Bot Extensions 📂 ({len(bot.extensions_list)})")
    print(bot.extensions_list)
    print("[-] Logged in as {0.user} 🤖".format(bot))
    print("[-] Startup Complete! 🟢")


@bot.event
async def on_guild_join(guild):
    print(f"➕ NEW GUILD: {guild.name} | id: {guild.id}")
@bot.event
async def on_guild_remove(guild):
    print(f"➖ REMOVED GUILD: {guild.name} | id: {guild.id}")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN, reconnect=True)
