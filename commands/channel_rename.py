import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks

# переименовать канал
class channel_rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Переименовать канал", dm_permission=False)
    @application_checks.guild_only()
    async def channel_rename(self, interaction: Interaction, name = SlashOption(description="Новое название"), channel_name: nextcord.TextChannel = SlashOption(description="Канал")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            await channel_name.edit(name=name)
            await interaction.response.send_message("Готово", ephemeral=True)
        
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(channel_rename(bot))