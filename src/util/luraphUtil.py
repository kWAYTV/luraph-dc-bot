import json, base64, os, requests, discord
from discord.ext import commands
from .config import Config
from colorama import Fore, init, Style
from datetime import datetime

class Luraph:

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

        with open("src/util/options.json", "r") as f:
            options = json.load(f)

        url = f"{self.endpoint}/obfuscate/new"

        request_body = {
            "fileName": filename,
            "node": node,
            "script": script.decode('utf-8'), # convert bytes to str
            "options": options,
        }

        response = requests.post(url, headers=self.headers, json=request_body)
        data = json.loads(response.text)
        return data["jobId"]

    async def check_status(self, jobId: str):
        url = f"{self.endpoint}/obfuscate/status/{jobId}"
        response = requests.get(url, headers=self.headers)
        if response.text == "" or response.text == True:
            return True
        else:
            data = json.loads(response.text)
            return data["status"]

    async def download_obfuscated(self, jobId: str, id: str):
        url = f"{self.endpoint}/obfuscate/download/{jobId}"
        response = requests.get(url, headers=self.headers)

        obfuscated_file_path = f"temp-{id}/obfuscated.lua"
        
        # Write the obfuscated file to a file
        with open(obfuscated_file_path, "wb") as f:
            f.write(response.content)
            print(f"{Fore.GREEN} > {Style.RESET_ALL}Wrote obfuscated file to {obfuscated_file_path}.")

        return True

