import discord, base64, os, requests
from discord.ext import commands
from colorama import Fore, Style
from discord import app_commands
from datetime import datetime
from src.util.luraphUtil import Luraph
from src.util.utils import Utils
from src.util.logger import Logger

class Obfuscate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Obfuscate command  
    @app_commands.command(name="obfuscate", description="Obfuscate your code.")
    @app_commands.checks.has_permissions(administrator=True)
    async def obfuscate_command(self, interaction: discord.Interaction, file: discord.Attachment = None, link: str = None):
        await interaction.response.defer(ephemeral=True)

        if file:
            mode = "file"
            filename = file.filename
        elif link:
            mode = "link"
            filename = link

        # Change the semaphore to True
        await Utils().change_semaphore(True)

        # Get semaphore status
        semaphore = await Utils().get_semaphore()
        if semaphore:
            await interaction.followup.send("❌ Sorry, but the bot is currently busy. Please try again later.", ephemeral=True)
            return

        # Filter if file exists
        if mode == "file" and not file:
            await interaction.followup.send("❌ Please provide a Lua file.", ephemeral=True)
            return
        if mode == "link" and not link:
            await interaction.followup.send("❌ Please provide a Lua file.", ephemeral=True)
            return

        await Logger(self.bot).log(f"Obfuscate command invoked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}).\n\nTo obfuscate file: {filename}.")
        await Logger(self.bot).send_warning(f"Obfuscate command invoked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}).\n\nTo obfuscate file: {filename}.")

        # Send a message to the user to make them wait
        await interaction.followup.send(f"✔️ Starting obfuscation...", ephemeral=True)

        tempdir = f"temp-{interaction.user.id}"

        # If the folder temp doesn't exist, create it
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Created temp folder for user.")
        else:
            # Remove the folder temp with all its contents
            for file in os.listdir(tempdir):
                os.remove(f"{tempdir}/{file}")
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Removed all files user had in 'temp'.")
            os.rmdir(tempdir)
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Removed user folder 'temp'.")
            os.mkdir(tempdir)
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Created user folder 'temp'.")
        
        # Retrieve the Lua file
        if mode == "file":
            attachment = await file.read()
            lua_file = attachment.decode()
        if mode == "link":
            lua_file = requests.get(link).content

        if not lua_file:
            await interaction.followup.send("❌ Error retrieving the Lua file.", ephemeral=True)
            await Utils().change_semaphore(False)
            # Delete the temporary files
            os.remove(to_obf_file_path)
            os.remove(obfuscated_file_path)
            os.rmdir(tempdir)
            return
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Retrieved Lua file: {filename}.")

        # Convert the Lua file to Base64
        lua_base64 = base64.b64encode(lua_file)
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Converted Lua file to Base64.")

        # Set paths
        to_obf_file_path = f"{tempdir}/to_obf.lua"
        obfuscated_file_path = f"{tempdir}/obfuscated.lua"

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
            await interaction.followup.send("❌ Error getting the recommended node.", ephemeral=True)
            await Utils().change_semaphore(False)
            # Delete the temporary files
            os.remove(to_obf_file_path)
            os.remove(obfuscated_file_path)
            os.rmdir(tempdir)
            return

        # Obfuscate the lua with luraph
        jobId = await Luraph(self.bot).obfuscate("obfuscated.lua", node, lua_base64, False)
        if not jobId == None:
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Started obfuscating Lua with job id: {jobId}")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error starting obfuscation.")
            await interaction.followup.send("❌ Error starting obfuscation.", ephemeral=True)
            await Utils().change_semaphore(False)
            # Delete the temporary files
            os.remove(to_obf_file_path)
            os.remove(obfuscated_file_path)
            os.rmdir(tempdir)
            return

        # Check the status of the obfuscation
        status = await Luraph(self.bot).check_status(jobId)
        if status == True:
            status = "Finished"
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Obfuscation status: {status}")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error on the status of job {jobId}: {status}")
            await interaction.followup.send(f"❌ Error on the status of job {jobId}: {status}", ephemeral=True)
            await Utils().change_semaphore(False)
            # Delete the temporary files
            os.remove(to_obf_file_path)
            os.remove(obfuscated_file_path)
            os.rmdir(tempdir)
            return

        # Download the obfuscated file
        obfuscated_file = await Luraph(self.bot).download_obfuscated(jobId, interaction.user.id)
        if obfuscated_file:
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Obfuscated file downloaded.")
        else:
            print(f"{Fore.RED} > {Style.RESET_ALL}Error downloading obfuscated file.")
            await interaction.followup.send("❌ Error downloading obfuscated file.")
            await Utils().change_semaphore(False)
            # Delete the temporary files
            os.remove(to_obf_file_path)
            os.remove(obfuscated_file_path)
            os.rmdir(tempdir)
            return
        
        # Send an embed to confirm the obfuscation
        embed = discord.Embed(title="Obfuscation done!", description="We've finished obfuscating your code.", color=0x00ff00)
        embed.add_field(name="Obfuscated file", value=f"`{filename}`", inline=False)
        embed.add_field(name="Job ID", value=f"`{jobId}`", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url="https://i.imgur.com/FdZlWFr.png")
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed, ephemeral=True)

        with open(obfuscated_file_path, "rb") as f:
            await interaction.followup.send(content="✔️ Here's your obfuscated code:", file=discord.File(f), ephemeral=True)

        print(f"{Fore.GREEN} > {Style.RESET_ALL}Sent obfuscated file to {interaction.user.name}#{interaction.user.discriminator}.")

        # Change the semaphore to False
        await Utils().change_semaphore(False)

        # Delete the temporary files
        os.remove(to_obf_file_path)
        os.remove(obfuscated_file_path)
        os.rmdir(tempdir)
        print(f"{Fore.GREEN} > {Style.RESET_ALL}Deleted temporary file(s) and folder(s).")

    @obfuscate_command.error
    async def obfuscate_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Obfuscate(bot))
    print(f"[{Fore.MAGENTA}INFO{Fore.RESET}] {Fore.GREEN}Loaded Obfuscate cog.{Fore.RESET}")
