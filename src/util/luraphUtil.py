import json, requests, discord
from discord.ext import commands
from .config import Config
from colorama import Fore, init, Style
from datetime import datetime

class Luraph():

    def __init__(self, bot: commands.Bot):
        self.endpoint = "https://api.lura.ph/v1"
        self.bot = bot
        self.headers = {
            'Luraph-API-Key': Config().luraph_api_key,
        }

    async def get_recommended_node(self):
        url = f"{self.endpoint}/obfuscate/nodes"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        return data["recommendedId"]
    
    async def obfuscate(self, filename: str, node: str, script: str, useTokens: bool):

        options = {
            "INTENSE_VM_STRUCTURE": true,
            "ENABLE_GC_FIXES": true,
            "TARGET_VERSION": "CS:GO",
            "VM_ENCRYPTION": true,
            "DISABLE_LINE_INFORMATION": true,
            "USE_DEBUG_LIBRARY": false,
        }

        url = f"{self.endpoint}/obfuscate/new?filename={filename}&node={node}&script={script}&options={options}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        return data["jobId"]
    
    async def check_status(self, jobId: str):
        url = f"{self.endpoint}/obfuscate/status/:{jobId}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        return data

    async def download_obfuscated(self, jobId: str):
        url = f"{self.endpoint}/obfuscate/download/:{jobId}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        return data["script"]
