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

    @nextcord.slash_command(description='Регистрация для участия в игре "Пидор дня"', dm_permission=False)
    @application_checks.guild_only()
    async def pidor_reg(self, interaction: Interaction):
            try:
                with open(pidors, 'r') as file:
                    ids = file.read().split()
            except FileNotFoundError:
                ids = []

            id = str(interaction.user.id)
            if id in ids:
                ids.remove(id)
                await interaction.response.send_message("Вы больше не участвуете в игре **Пидор дня**. *(на всех серверах где есть Вы и Lucy)*")
            else:
                ids.append(id)
                await interaction.response.send_message("Вы берете участвие в игре **Пидор дня**. *(на всех серверах где есть Вы и Lucy)*")

            with open(pidors, 'w') as file:
                file.write(' '.join(ids))

    @nextcord.slash_command(description="Пидор дня", dm_permission=False)
    @application_checks.guild_only()
    async def pidor(self, interaction: Interaction):
        await interaction.response.defer()
        server_id = interaction.guild.id
        server_data = get_server_data(server_id)
        date = datetime.date.today()
        id = str(interaction.user.id)
        try:
            with open(pidors, 'r') as file:
                list_id = file.read().split()
        except FileNotFoundError:
            list_id = []
        if id in list_id:
            if server_data['date'] is None or server_data['date'] != date:
                server_data['date'] = date
                pidor = None
                members = interaction.guild.humans
                #while(True):
                for attempt in range(len(list_id)+len(members)):
                    pidor = random.choice(members)
                    pidor_id = str(pidor.id)
                    if pidor_id in list_id:
                        break
                    else:
                        pidor = None

                if pidor is not None:
                    rand = random.randrange(1, 5)
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
        else:
            await interaction.followup.send("Для регистрации используйте **/pidor_reg**")

def setup(bot):
    bot.add_cog(pidor(bot))