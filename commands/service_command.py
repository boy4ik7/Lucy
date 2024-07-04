import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import os
import sys
from datetime import datetime

TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT
NATIVE_GUILD_ID = 425001135242346497 # Server Server
GUILD_2_ID = 756101274243432471 # Хайповые козырьки

class service_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# остановить бота
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Сервисные команды (только для разработчика)")
    async def service_command(self, interaction: Interaction, command: str = SlashOption(description="Доступные команды: reboot, stop")):
        if interaction.user.id == 412971979650629634:
            if command == "reboot":
                await interaction.response.send_message("Перезагрузка ♻️", ephemeral=True)
                print('Бот остановлен. Перезагрузка...')
                time = datetime.now().time().strftime("%H:%M")
                gild_id = self.bot.get_guild(1089166037934669966)
                log_channel = 1107761340031979592
                await gild_id.get_channel(log_channel).send(time + " - Бот ушел на перезагрузку.")
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif command == "stop":
                await interaction.response.send_message("Бот остановлен.", ephemeral=True)
                print('Бот остановлен.')
                time = datetime.now().time().strftime("%H:%M")
                gild_id = self.bot.get_guild(1089166037934669966)
                log_channel = 1107761340031979592
                await gild_id.get_channel(log_channel).send(time + " - Бот остановлен.")
                quit()
            else:
                await interaction.response.send_message("Не верная команда", ephemeral=True)
        else:
            await interaction.response.send_message("Нету прав", ephemeral=True)
    
    @service_command.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.send("Ошибка.", ephemeral=True)
    
def setup(bot):
    bot.add_cog(service_command(bot))