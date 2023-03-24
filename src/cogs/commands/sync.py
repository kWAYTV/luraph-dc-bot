from discord.ext import commands
from colorama import Fore

class SyncCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await self.bot.tree.sync()
        msg = await ctx.send("Successfully synced slash commands!")
        print(f"{Fore.GREEN}>{Fore.WHITE} Successfully synced slash commands!")
        await msg.delete()
        return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SyncCommand(bot))
    return print(f"[{Fore.MAGENTA}INFO{Fore.RESET}] {Fore.GREEN}Successfully loaded sync cog.{Fore.RESET}")