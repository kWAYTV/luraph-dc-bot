import discord, requests, base64, os
from src.util.config import Config
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from src.util.luraphUtil import Luraph

class Obfuscate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Obfuscate command  
    @app_commands.command(name="obfuscate", description="Obfuscate your code.")
    async def obfuscate_command(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer(ephemeral=True)
        
        # Retrieve the Lua file from the specified URL
        lua_file = requests.get(link).content

        # Convert the Lua file to Base64
        lua_base64 = base64.b64encode(lua_file)

        # If the folder data doesn't exist, create it
        if not os.path.exists("temp"):
            os.mkdir("temp")

        # Write the obfuscated Lua code to a file
        file_path = "temp/obfuscated.lua"
        with open(file_path, "wb") as f:
            f.write(lua_base64)

        # Obfuscate the lua with luraph
        
        # Send an embed to confirm the obfuscation
        with open(file_path, "rb") as send_file:
            embed = discord.Embed(title="Obfuscation done!", description="We've finished obfuscating your code.", color=0x00ff00)
            embed.add_field(name="Obfuscated from", value=f"`{link}`")
            embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url="https://i.imgur.com/FdZlWFr.png")
            embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, file=discord.File(send_file))

        # Delete the temporary file
        os.remove(file_path)

    @obfuscate_command.error
    async def obfuscate_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Obfuscate(bot))
