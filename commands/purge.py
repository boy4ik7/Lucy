import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import time

# очистить сообщения
class purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description = "Удалить сообщения", dm_permission=False)
    @application_checks.guild_only()
    async def purge(self, interaction: Interaction, amount : int = SlashOption(description = "Сколько сообщений удалить? (Не больше 100 за раз)")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            if amount < 0:
                await interaction.response.send_message("Удаляем 0 сообщений.", ephemeral=True)
            if amount <= 100:
                await interaction.response.send_message("Удаляем.", ephemeral=True)
                time.sleep(1)
                await interaction.channel.purge(limit=amount)
            if amount > 100:
                await interaction.response.send_message("Больше 100 нельзя.", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав.", ephemeral=True)
    
    @purge.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.response.send_message("Недостаточно прав.", ephemeral=True)

def setup(bot):
    bot.add_cog(purge(bot))