from urllib.parse import quote_plus
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import random, requests
import time
import json
import asyncio
 
TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

class example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description = "Описание команды")
    #@application_checks.dm_only()
    async def example(self, interaction: Interaction):
        await interaction.response.send_message("Пример")

def setup(bot):
    bot.add_cog(example(bot))
