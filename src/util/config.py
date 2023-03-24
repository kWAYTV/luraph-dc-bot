from yaml import SafeLoader
import yaml 
import sys

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.discord_token = self.config["DISCORD_TOKEN"]
            self.bot_prefix = self.config["PREFIX"]
            self.logs_channel = int(self.config["LOGS_CHANNEL"])
            self.luraph_api_key = self.config["LURAPH_API_KEY"]