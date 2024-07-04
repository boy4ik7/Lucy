import nextcord
import platform
import os
from nextcord import Interaction
from nextcord.ext import commands, application_checks
import psutil

TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

class status_server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Статус сервера")
    @application_checks.guild_only()
    async def status(self, interaction: Interaction):
        await interaction.response.defer()
        cpu_usage = int(psutil.cpu_percent(interval=1))
        if cpu_usage == 0:
            cpu_usage = "*Недоступно*"
        else:
            cpu_usage = str(cpu_usage) + "%"
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        system = platform.system()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()
        if processor == machine:
            processor = "*Недоступно*"
        platform_info = platform.platform()
        python_version = platform.python_version()
        ping = int(self.bot.latency * 1000)
        info = nextcord.Embed(
            title="Lucy BOT",
            description=
                "**CPU**\n"
                f"Процессор: {processor}\n"
                f"Архитектура: {machine}\n"
                f"Используется: {cpu_usage}\n"
                "**ОЗУ\n**"
                f"Всего: {memory_info.total / (1024 ** 3):.2f} Гб\n"
                f"Свободно: {memory_info.available / (1024 ** 3):.2f} Гб\n"
                f"Используется: {memory_info.used / (1024 ** 3):.2f} Гб ({int(memory_info.percent)}%)\n"
                "**ПЗУ\n**"
                f"Всего: {disk_usage.total / (1024 ** 3):.2f} Гб\n"
                f"Занято: {disk_usage.used / (1024 ** 3):.2f} Гб\n"
                "**СИСТЕМА**\n"
                f"OS: {system}\n"
                f"Версия: {version}\n"
                f"Платформа: {platform_info}\n"
                "**PYTHON\n**"
                f"Версия: {python_version}\n"
                "**СЕТЬ\n**"
                f"Передано: {net_io.bytes_sent / (1024 ** 2):.2f} Мб\n"
                f"Получено: {net_io.bytes_recv / (1024 ** 2):.2f} Мб\n"
                f"Пинг: {ping} Мс\n",
            color=nextcord.Color.green())
        info.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.followup.send(embed=info)

    '''

    def get_temp(self):
        thermal_zones = [f for f in os.listdir('/sys/class/thermal') if f.startswith('thermal_zone')]
        temps = {}
        for zone in thermal_zones:
            with open(f'/sys/class/thermal/{zone}/temp', 'r') as file:
                temp = int(file.read()) / 1000
                temps[zone] = temp
        return temps

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Температуры")
    @application_checks.guild_only()
    async def temperature(self, interaction: Interaction):
        await interaction.response.defer()
        system = platform.system()
        if system == "Linux":
            temperature = "```Температуры\n"
            temperatures = self.get_temp()
            for zone, temp in temperatures.items():
                temperature += (f'{zone}: {temp}°C\n')
            temperature += "```"
            await interaction.followup.send(temperature)
        else:
            await interaction.followup.send(f"{system}", ephemeral=True)
    '''
def setup(bot):
    bot.add_cog(status_server(bot))