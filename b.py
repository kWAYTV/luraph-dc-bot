# Imports
import discord, os
from discord.ext import commands
from colorama import Fore
from src.helper.config import Config

class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        print(f"[{Fore.MAGENTA}INFO{Fore.RESET}] {Fore.GREEN}Starting bot...{Fore.RESET}")
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Loading cogs...")
        for filename in os.listdir("./src/cogs/commands"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.commands.{filename[:-3]}")
        for filename in os.listdir("./src/cogs/events"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.events.{filename[:-3]}")
        for filename in os.listdir("./src/cogs/loops"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.loops.{filename[:-3]}")

# Define the clients
bot = Bot(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

if __name__ == "__main__":
    try:
        bot.run(Config().discord_token)
    except KeyboardInterrupt:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Powering off the bot...")
        exit()