import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks

# удалить канал
class channel_delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description=" Удалить канал", dm_permission=False)
    @application_checks.guild_only()
    async def channel_delete(self, interaction: Interaction, channel_name: nextcord.TextChannel = SlashOption(description="Канал")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            await channel_name.delete()
            await interaction.response.send_message("Готово", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(channel_delete(bot))