# Imports
import discord, os, time, requests, json, logging, asyncio
from discord.ext.commands import CommandNotFound
from pystyle import Colors, Colorate, Center
from discord.ext import commands, tasks
from colorama import Fore, init, Style
from src.util.config import Config
from datetime import datetime
from itertools import cycle
from threading import Timer

logo = """
██╗     ██╗   ██╗██████╗  █████╗ ██████╗ ██╗  ██╗
██║     ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║  ██║
██║     ██║   ██║██████╔╝███████║██████╔╝███████║
██║     ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║
███████╗╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝"""

# Clear function
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this.
clear()

def printLogo():
    print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
    print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "-----------------------------------------------------------\n\n", 1)))

class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Starting bot...")
        for filename in os.listdir("./src/cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}] {Fore.RESET}Slash command detected: {filename[:-3]}")
                await self.load_extension(f"src.cogs.{filename[:-3]}")

# Define the clients
bot = Bot(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

# Dynamic activity
status = cycle(["security", "obfuscation", "protection", "development"])
@tasks.loop(seconds=30)
async def changeStatus():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

# On Ready Event
@bot.event
async def on_ready():
    clear()
    printLogo()
    print(f"{Fore.MAGENTA}> {Fore.RESET}Logged in as {bot.user.name}#{bot.user.discriminator}.")

    logging.basicConfig(handlers=[logging.FileHandler('luraph.log', 'a+', 'utf-8')], level=logging.ERROR, format='%(asctime)s: %(message)s')

    await changeStatus.start()

# Sync slash commands
@bot.command()
async def sync(ctx):
    try:
        await ctx.message.delete()
        await bot.tree.sync()
        msg = await ctx.send("Done!")
        time.sleep(2)
        await msg.delete()
        print(f"{Fore.GREEN}>{Fore.WHITE} Slash commands synced!")
    except Exception as e:
        print(f"{Fore.RED}>{Fore.WHITE} Error syncing slash commands: {e}")

if __name__ == "__main__":
    try:
        bot.run(Config().discord_token)
    except KeyboardInterrupt:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Powering off the bot...")
        exit()