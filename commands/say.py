import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# отправить сообщение от имени бота (в этом же канале)
class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Напишет сообщение", dm_permission=False)
    async def say(self, interaction: Interaction, text: str = SlashOption(description="Текст сообщения")):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            await interaction.response.send_message("Готово", ephemeral=True)
            await interaction.channel.send(text)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(say(bot))