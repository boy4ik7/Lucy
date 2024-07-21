import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks
import random
#import time
import asyncio
import datetime

# игра пидор дня
pidors = "pidors_base.txt"
server_data = {}
def get_server_data(server_id):
    if server_id not in server_data:
        add_server(server_id)
    return server_data[server_id]

def add_server(server_id):
    server_data[server_id] = {
        'date': None
    }

class pidor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Пидор дня", dm_permission=False)
    @application_checks.guild_only()
    async def pidor(self, interaction: Interaction):
        await interaction.response.defer()
        server_id = interaction.guild.id
        server_data = get_server_data(server_id)
        date = datetime.date.today()
        if server_data['date'] is None or server_data['date'] != date:
            server_data['date'] = date
            pidor = None
            members = interaction.guild.humans
            pidor = random.choice(members)
            if pidor is not None:
                rand = random.randrange(1, 7)
                if rand == 1:
                    await interaction.followup.send("Кто же пидор дня? 🤨")
                    n = 4
                    for i in range(3):
                        n -=  1 
                        await interaction.channel.send(n)
                        #time.sleep(1)
                        await asyncio.sleep(1)
                    await interaction.channel.send("Пидор дня - " + pidor.mention)
                elif rand == 2:
                    await interaction.followup.send("Система поиска пидорасов активирована 📍")
                    await interaction.channel.send("Бип 🔈")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Бииип 🔉")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Биииииииип 🔊")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Пидор обнаружен 👀 " + pidor.mention)
                elif rand == 3:
                    await interaction.followup.send("Звонят, просят пидора 📳")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Вас к телефону 📱 " + pidor.mention)
                elif rand == 4:
                    await interaction.followup.send("Колдуем 🪄")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Вжух вжух ✨")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send(".∧＿∧ \n"
                    "( ･ω･｡)つ━☆・*。 \n"
                    "⊂  ノ    ・゜+. \n"
                    "しーＪ   °。+ *´¨) \n"
                    "         .· ´¸.·*´¨) \n"
                    "          (¸.·´ (¸.·'* ☆ ВЖУХ И ТЫ ПИДОР, " + pidor.mention)
                elif rand == 5:
                    await interaction.followup.send("Мне сказали у вас тут пидор")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("# Не ну к нему я бы на вашем месте спиною не поворачивался - " + pidor.mention)
                elif rand == 6:
                    await interaction.followup.send("Не будем показывать пальцем...")
                    #time.sleep(1)
                    await asyncio.sleep(1)
                    await interaction.channel.send("Но...")
                    await asyncio.sleep(1)
                    await interaction.channel.send("👉 " + pidor.mention)
                elif rand == 7:
                    await asyncio.sleep(1)
                    await interaction.followup.send("# ВНИМАНИЕ " + pidor.mention + "ПИДОР!")
                    
            else:
                await interaction.followup.send("Сегодня нет пидора 😮")
        else:
            await interaction.followup.send("Сегодня уже выбран счастливчик, приходите завтра.")
        
def setup(bot):
    bot.add_cog(pidor(bot))