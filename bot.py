import nextcord
from nextcord.ext import commands
import os
from datetime import datetime, date

description = """Lucy BOT"""

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds=True
intents.voice_states=True

bot = commands.Bot(command_prefix="!", description=description, intents=intents, help_command=None)

''' события '''
# запуск бота
@bot.event
async def on_ready(): 
    time = datetime.now().time().strftime("%H:%M")
    await bot.change_presence(activity=nextcord.Activity(name="музыку", type=nextcord.ActivityType.listening))
    print(datetime.now().time().strftime("%H:%M"), date.today(), f"{bot.user} - Бот запущен.")
    gild_id = bot.get_guild(1089166037934669966)
    log_channel = 1107761340031979592
    await gild_id.get_channel(log_channel).send(time + " - Бот запущен.")

''' проверка доступных событий '''
events_directory = os.path.abspath('./events')
print("События:")
for f in os.listdir(events_directory):
	if f.endswith(".py"):
		print(f)
		bot.load_extension("events." + f[:-3])

''' проверка доступных команд '''
slash_command_directory = os.path.abspath('./commands')
print("Команды:")
for f in os.listdir(slash_command_directory):
	if f.endswith(".py"):
		print(f)
		bot.load_extension("commands." + f[:-3])

''' проверка доступных тестовых команд '''
''' '''
command_directory = os.path.abspath('./test_commands')
print("Тестовые команды:")
for f in os.listdir(command_directory):
	if f.endswith(".py"):
		print(f)
		bot.load_extension("test_commands." + f[:-3])

token = ""
bot.run(token)
