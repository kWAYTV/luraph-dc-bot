from discord.ext import commands, tasks
from colorama import Fore
from itertools import cycle
import discord

class StatusLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.changeStatus.start()

    # Dynamic activity
    status = cycle(["security", "obfuscation", "protection", "development"])
    @tasks.loop(seconds=30)
    async def changeStatus(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=next(self.status)))

    @changeStatus.before_loop
    async def before_changeStatus(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusLoop(bot))
    return print(f"{Fore.GREEN}> {Fore.RESET}Status loop loaded!")