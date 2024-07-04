import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks

# дать ссылку-приглашение на сервер
class give_invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Дать ссылку-приглашение на сервер", dm_permission=False)
    @application_checks.guild_only()
    async def give_invite(self, interaction: Interaction):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            invite = await interaction.channel.create_invite(max_age=0, max_uses = 1, temporary=True)
            await interaction.channel.send(invite)
            await interaction.response.send_message("Готово", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(give_invite(bot))