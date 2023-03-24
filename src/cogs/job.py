import discord, json
from src.util.config import Config
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from colorama import Fore, init, Style
from src.util.luraphUtil import Luraph
from src.util.utils import Utils

class Job(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Ping bot command  
    @app_commands.command(name="job", description="Check the status from a luraph job.")
    @app_commands.checks.has_permissions(administrator=True)
    async def job_command(self, interaction: discord.Interaction, jobid: str):
        await interaction.response.defer(ephemeral=True)
        
        # Send a message to the user to make them wait
        await interaction.followup.send(f"Checking job with id `{jobid}`...")

        # Check the status of the job
        status = await Luraph(self.bot).check_status(jobid)
        if status:
            status = "Finished"
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Finished checking status of job {jobid}.")
        else:
            status = json.loads(status)
            status = status["error"]
            print(f"{Fore.RED} > {Style.RESET_ALL}Error on the status of job {jobid}: {status}")

        # Create embed
        embed = discord.Embed(title="Checking done!", description="We've finished checking the status of your job.", color=0x00ff00)
        embed.add_field(name="Checked Job ID", value=f"`{jobid}`", inline=False)
        embed.add_field(name="Status", value=f"`{status}`", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url="https://i.imgur.com/FdZlWFr.png")
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed, ephemeral=True)

        print(f"{Fore.GREEN} > {Style.RESET_ALL}Sent status to {interaction.user.name}#{interaction.user.discriminator}.")

        await Utils(self.bot).log(f"Job command invoked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}).{interaction.user.name}#{interaction.user.discriminator} checked the status of job `{jobid}`. Status: `{status}`")

    @job_command.error
    async def job_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Job(bot))