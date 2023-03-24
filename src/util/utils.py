import json, base64, os, requests, discord
from discord.ext import commands
from .config import Config
from colorama import Fore, init, Style
from datetime import datetime

class Utils:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def log(self, description: str):
        channel = self.bot.get_channel(Config().logs_channel)
        embed = discord.Embed(title="Luraph Bot", description=description)
        embed.set_thumbnail(url="https://i.imgur.com/FdZlWFr.png")
        embed.set_footer(text=f"Luraph Bot - discord.gg/kws")
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)