import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks

TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

class edit_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Установить статус бота")
    @application_checks.guild_only()
    async def set_status(self, interaction: Interaction, status: str = SlashOption(description="Статус", required = False), activity : str = SlashOption(description="Активность", choices= ["Свой", "Играет в", "Стримит", "Слушает", "Смотрит", "Соревнуется", "Убрать"], default="Свой", required = False), url : str = SlashOption(description="Ссылка для стрима",  default="", required = False)):
        if interaction.user.guild_permissions.administrator or interaction.user.id == 412971979650629634:
            if activity == "Свой":
                activity = nextcord.CustomActivity(name=status)
            elif activity == "Играет в":
                activity = nextcord.Game(name=status)
            elif activity == "Стримит": 
                activity = nextcord.Streaming(name=status, url=url)
            elif activity == "Слушает":
                activity = nextcord.Activity(name=status, type=nextcord.ActivityType.listening)
            elif activity == "Смотрит":
                activity = nextcord.Activity(name=status, type=nextcord.ActivityType.watching)
            elif activity == "Соревнуется":
                activity = nextcord.Activity(name=status, type=nextcord.ActivityType.competing)
            elif activity == "Убрать":
                activity = nextcord.Activity(name=status, type=nextcord.ActivityType.unknown)
            await self.bot.change_presence(activity=activity)
            await interaction.response.send_message("Готово.", ephemeral=True)
        else:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(edit_status(bot))