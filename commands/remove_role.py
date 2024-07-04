import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks

# убрать роль
class remove_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Убрать роль", dm_permission=False)
    @application_checks.guild_only()
    async def remove_role(self, interaction: Interaction, role: nextcord.Role = SlashOption(description="Название роли"), user: nextcord.User = SlashOption(description="У:")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            await user.remove_roles(role)
            await interaction.response.send_message("Готово", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)
    
    @remove_role.error
    async def info_error(self, interaction: Interaction, error):
        await interaction.response.send_message("Недостаточно прав.", ephemeral=True)

def setup(bot):
    bot.add_cog(remove_role(bot))