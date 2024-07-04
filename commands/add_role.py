import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks

# дать роль
class add_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Дать роль", dm_permission=False)
    @application_checks.guild_only()
    async def add_role(self, interaction: Interaction, role: nextcord.Role = SlashOption(description="Название роли"), user: nextcord.User = SlashOption(description="Кому:")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            #role = interaction.guild.get_role(role_id)
            await user.add_roles(role)
            await interaction.response.send_message("Готово", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(add_role(bot))