from nextcord.ext import commands

 # пришло личное сообщение
 # создал для примера и переноса последующих команд
TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT
NATIVE_GUILD_ID = 425001135242346497 # Server Server
GUILD_2_ID = 756101274243432471 # Хайповые козырьки

class new_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild and (message.author.id != 498879255468572675) and (message.author.id != 412971979650629634):
            print("Пришло личное сообщение: |" ,message.content, "| от |", message.author, "|")
            user = self.bot.get_user(412971979650629634)
            author = str(message.author)
            message = message.content
            await user.send("Сообщение от: "+author)
            await user.send(message)

def setup(bot):
    bot.add_cog(new_message(bot))