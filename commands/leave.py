import nextcord
from nextcord import Interaction
from nextcord.ext import commands

 
 # создал для примера и переноса последующих команд
TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], description="Покинуть сервер")
    async def leave(self, interaction: Interaction):
        guilds = self.bot.guilds
        bot = self.bot
        view = self.leave_server_select(bot, guilds)
        await interaction.response.send_message(view=view) 

    class leave_server_select(nextcord.ui.View):
        def __init__(self, bot, guilds):
            super().__init__(
                timeout= 30,
            )
            self.bot = bot
            self.guilds = guilds
             
            self.select = nextcord.ui.StringSelect( 
                placeholder = "Выберите сервер из которого выйдет бот",
                min_values = 1,
                max_values = 1,
                options = [ 
                    nextcord.SelectOption(
                        label=f"{guild.name}",
                        value=f"{guild.id}+{guild.name}"
                    ) for guild in self.guilds
                ]
            )
            
            self.select.callback = self.select_callback
            self.add_item(self.select)


        async def select_callback(self, select):
            data = self.select.values[0].split("+")
            server_name = data[1] + " ID:" + data[0]
            guild_id = int(data[0])
            guild = self.bot.get_guild(guild_id)
            try:
                await guild.leave()
                await select.channel.send(f"Бот покинул - {server_name}")
            except:
                await select.channel.send("Ошибка.")


def setup(bot):
    bot.add_cog(leave(bot))