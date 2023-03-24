import discord
from discord.ext import commands
from src.config.config import Config
from datetime import datetime

class Logger:

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def log(self, description: str):
            channel = self.bot.get_channel(Config().logs_channel)
            embed = discord.Embed(title="Luraph Bot", description=description)
            embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
            embed.set_footer(text=f"Luraph Bot - discord.gg/kws")
            embed.timestamp = datetime.utcnow()
            await channel.send(embed=embed)

    async def send_warning(self, message: str):
        embed = discord.Embed(title="Luraph Bot", description=message)
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.set_footer(text=f"Luraph Bot - discord.gg/kws")
        embed.timestamp = datetime.utcnow()
        for member_id in Config().warn_members:
            member = await self.bot.fetch_user(member_id)
            if member:
                try:
                    await member.send(embed = embed)
                except discord.errors.Forbidden:
                    await self.log(f"Failed to send a warning message to user {member.id} due to privacy settings.")
            else:
                await self.log(f"Failed to send a warning message to user {member_id} due to invalid user.")