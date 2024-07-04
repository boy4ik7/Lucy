import urllib.request
import io
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests
import random

TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

# рулетка с загрузкой файлов на сервер
class rule34_unload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Та же рулетка, только с загрузкой изображений и видеофайлов на сервер")
    async def rule34_unload(self, interaction: Interaction, tags: str = SlashOption(description="Тег")):
        url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index"
        params = {
            "tags": tags,
            "limit": 1000,
            "json": 1
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            await interaction.response.defer()
            data = response.json()
            le = len(data)
            index = random.randint(0, le - 1)
            file_url = data[index]['file_url']
            response = requests.head(file_url)
            if response.status_code == 200:
                content_length = response.headers.get("content-length")
                if content_length:
                    file_size = int(content_length) / 1024 / 1024
                    if file_size < 25:
                        format = file_url.split(".")
                        format = format[3]
                        file = urllib.request.urlopen(file_url).read()
                        file = io.BytesIO(file)
                        await interaction.followup.send("По запросу: "+ tags,file=nextcord.File(file, filename= f"file.{format}"))
                    else:
                        await interaction.followup.send("Файл слишком большой, ссылка на файл: \n"+ file_url)
                else:
                    await interaction.followup.send("Произошла ошибка при обработке запроса.")
            else:
                await interaction.followup.send("Произошла ошибка при обработке запроса.")
            
        else:
            await interaction.response.send_message("Произошла ошибка при обработке запроса.")
    
    @rule34_unload.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.channel.send("Ничего не найдено по вашему запросу.")

def setup(bot):
    bot.add_cog(rule34_unload(bot))