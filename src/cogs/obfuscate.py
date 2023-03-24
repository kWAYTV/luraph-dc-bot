import discord, requests, base64, os, json
from src.util.config import Config
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from colorama import Fore, init, Style
from discord import app_commands
from datetime import datetime
from src.util.luraphUtil import Luraph
from src.util.utils import Utils

class Obfuscate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Obfuscate command  
    @app_commands.command(name="obfuscate", description="Obfuscate your code.")
    @app_commands.checks.has_permissions(administrator=True)
    async def obfuscate_command(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer(ephemeral=True)

        await Utils().log(f"{Fore.GREEN} > {Style.RESET_ALL}Obfuscate command invoked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}).")

        # If the folder data doesn't exist, create it
        if not os.path.exists("temp"):
            os.mkdir("temp")
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Created folder 'temp'.")
        
        # Retrieve the Lua file from the specified URL
        lua_file = requests.get(link).content
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Retrieved Lua file from {link}.")

        # Convert the Lua file to Base64
        lua_base64 = base64.b64encode(lua_file)
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Converted Lua file to Base64.")

        # Set paths
        to_obf_file_path = "temp/to_obf.lua"
        obfuscated_file_path = "temp/obfuscated.lua"

        # Write the obfuscated Lua code to a file
        with open(to_obf_file_path, "wb") as f:
            f.write(lua_base64)
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Wrote Lua file to {to_obf_file_path}.")

        # Get the recommended node
        node = await Luraph(self.bot).get_recommended_node()
        if not node == None:
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Got recommended node: {node}")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error getting the recommended node.")
            await interaction.followup.send("Error getting the recommended node.")
            return

        # Obfuscate the lua with luraph
        jobId = await Luraph(self.bot).obfuscate("obfuscated.lua", node, lua_base64, False)
        if not jobId == None:
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Started obfuscating Lua with job id: {jobId}")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error starting obfuscation.")
            await interaction.followup.send("Error starting obfuscation.")
            return

        # Check the status of the obfuscation
        status = await Luraph(self.bot).check_status(jobId)
        if status:
            status = "Finished"
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Obfuscation status: {status}")
        else:
            status = json.loads(status)
            status = status["error"]
            print(f"{Fore.RED} > {Style.RESET_ALL}Error on the status of job {jobid}: {status}")
            await interaction.followup.send(f"Error on the status of job {jobid}: {status}")
            return

        # Download the obfuscated file
        obfuscated_file = await Luraph(self.bot).download_obfuscated(jobId)
        if obfuscated_file:
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Obfuscated file downloaded.")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error downloading obfuscated file.")
            await interaction.followup.send("Error downloading obfuscated file.")
            return
        
        # Send an embed to confirm the obfuscation
        embed = discord.Embed(title="Obfuscation done!", description="We've finished obfuscating your code.", color=0x00ff00)
        embed.add_field(name="Obfuscated from", value=f"`{link}`", inline=False)
        embed.add_field(name="Job ID", value=f"`{jobId}`", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url="https://i.imgur.com/FdZlWFr.png")
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed)

        with open(obfuscated_file_path, "rb") as f:
            await interaction.followup.send(content="Here's your obfuscated code:", file=discord.File(f), ephemeral=True)

        print(f"{Fore.GREEN} > {Style.RESET_ALL}Sent obfuscated file to {interaction.user.name}#{interaction.user.discriminator}.")

        # Delete the temporary files
        os.remove(to_obf_file_path)
        os.remove(obfuscated_file_path)
        os.rmdir("temp")
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Deleted temporary file(s) and folder(s).")

    @obfuscate_command.error
    async def obfuscate_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Obfuscate(bot))
