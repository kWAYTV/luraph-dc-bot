import discord, json
from src.util.config import Config
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from colorama import Fore, init, Style
from src.util.luraphUtil import Luraph
from src.util.utils import Utils

class Download(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Ping bot command  
    @app_commands.command(name="download", description="Download a recent luraph job.")
    @app_commands.checks.has_permissions(administrator=True)
    async def download_command(self, interaction: discord.Interaction, jobid: str):
        await interaction.response.defer(ephemeral=True)

        # Change the semaphore to True
        await Utils(self.bot).change_semaphore(True)

        # Get semaphore status
        semaphore = await Utils(self.bot).get_semaphore()
        if semaphore:
            await interaction.followup.send("Sorry, but the bot is currently busy. Please try again later.", ephemeral=True)
            return

        # Send a message to the user to make them wait
        await interaction.followup.send(f"Downloading job with id `{jobid}`...")

        # Check the status of the job
        status = await Luraph(self.bot).download_obfuscated(jobid, interaction.user.id)

        # Create embed
        embed = discord.Embed(title="Download done!", description="We've finished downloading your job.", color=0x00ff00)
        embed.add_field(name="Downloaded Job ID", value=f"`{jobid}`", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url="https://i.imgur.com/FdZlWFr.png")
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed, ephemeral=True)

        # Send the obfuscated file to the user
        with open(obfuscated_file_path, "rb") as f:
            await interaction.followup.send(content="Here's your obfuscated code:", file=discord.File(f), ephemeral=True)

        print(f"{Fore.GREEN} > {Style.RESET_ALL}Sent obfuscated file to {interaction.user.name}#{interaction.user.discriminator}.")

        await Utils(self.bot).log(f"Download command invoked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}).{interaction.user.name}#{interaction.user.discriminator} checked the status of job `{jobid}`. Status: `{status}`")

        # Change the semaphore to False
        await Utils(self.bot).change_semaphore(False)

    @download_command.error
    async def download_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Download(bot))