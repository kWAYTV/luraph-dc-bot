from discord.ext import commands
from colorama import Fore
from pystyle import Colors, Colorate, Center
import os, logging

logo = """
██╗     ██╗   ██╗██████╗  █████╗ ██████╗ ██╗  ██╗
██║     ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║  ██║
██║     ██║   ██║██████╔╝███████║██████╔╝███████║
██║     ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║
███████╗╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝"""

# Clear function
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this.
def printLogo():
    print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
    print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "-----------------------------------------------------------\n\n", 1)))

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        clear()
        printLogo()
        print(f"{Fore.MAGENTA}> {Fore.RESET}Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")

        logging.basicConfig(handlers=[logging.FileHandler('luraph.log', 'a+', 'utf-8')], level=logging.ERROR, format='%(asctime)s: %(message)s')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
    return print(f"[{Fore.MAGENTA}INFO{Fore.RESET}] {Fore.GREEN}Events handler loaded!")