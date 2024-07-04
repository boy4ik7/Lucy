import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import random

formats_image = [".png", ".jpg", ".jpeg"]

# рулетка для префикс команд
class rule34_prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Рулетка")
    async def rule34(self, ctx, tags: str = None):
        if tags is None:
            await ctx.send("Введите тег после команды, *rule34 [Тег или теги через пробел]*")
        elif "video" in tags:
            await ctx.send("Тег video нельзя.")
        else:
            url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index"
            params = {
                "tags": tags,
                "limit": 1000,
                "json": 1
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                le = len(data)
                for i in range(20):
                    index = random.randint(0, le - 1)
                    image = data[index]['file_url']
                    if any(image.endswith(format) for format in formats_image):
                        break
                embed = nextcord.Embed(
                title = "По запросу: "+ tags,
                colour = nextcord.Color.green()
                    )
                embed.set_image(
                    url = image
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Произошла ошибка при обработке запроса.")
    
    @rule34.error
    async def info_error(self, ctx, error):
        await ctx.send("Ничего не найдено по вашему запросу.")
    
    @nextcord.slash_command(name="rule34", description="Поиск случайного изображения по тегу/тегам(через пробел) на Rule34")
    @application_checks.guild_only()
    async def rule34_(self, interaction: Interaction, tags : str = SlashOption(description="Тег")):
        if "video" in tags:
            await interaction.response.send_message("Тег video нельзя.", ephemeral=True)
        else:
            url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index"
            params = {
                "tags": tags,
                "limit": 1000,
                "json": 1
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                le = len(data)
                for i in range(20):
                    index = random.randint(0,  le - 1)
                    image = data[index]['file_url']
                    if any(image.endswith(format) for format in formats_image):
                        break
                embed = nextcord.Embed(
                title = "По запросу: "+ tags,
                colour = nextcord.Color.green()
                    )
                embed.set_image(
                    url = image
                    )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Произошла ошибка при обработке запроса.")
    
    @rule34_.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.channel.send("Ничего не найдено по вашему запросу.")

def setup(bot):
    bot.add_cog(rule34_prefix(bot))