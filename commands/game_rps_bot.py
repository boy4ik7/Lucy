import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import random

# камень, ножницы, бумага с ботом (только лс)
class RPCBOT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(description = "Камень ножницы бумага с ботом", dm_permission = True)
    #@application_checks.dm_only()
    async def game_rps_bot(self, interaction: Interaction):
        view = rps_bot()
        mes = await interaction.response.send_message("Выберите предмет:", view=view)
        await view.wait()
        list = [1, 2, 3]
        bot_choice = random.choice(list)
        if view.player_choice is not None:
            # все случаи камня
            if view.player_choice == 1 and bot_choice == 2:
               await mes.edit(content = self.bot.user.mention+" Выбрал ножницы")
               await interaction.channel.send("Вы победили")
            if view.player_choice == 2 and bot_choice == 1:
                await mes.edit(content = self.bot.user.mention+" Выбрал бумагу")
                await interaction.channel.send("Вы проиграли")
            if view.player_choice == 1 and bot_choice == 1:
                await mes.edit(content = self.bot.user.mention+" Выбрал камень")
                await interaction.channel.send("Ничья")
            # все случаи ножниц
            if view.player_choice == 2 and bot_choice == 3:
                await mes.edit(content = self.bot.user.mention+" Выбрал бумагу")
                await interaction.channel.send("Вы победили")
            if view.player_choice == 3 and bot_choice == 2:
                await mes.edit(content = self.bot.user.mention+" Выбрал ножницы")
                await interaction.channel.send("Вы проиграли")
            if view.player_choice == 2 and bot_choice == 2:
                await mes.edit(content = self.bot.user.mention+" Выбрал ножницы")
                await interaction.channel.send("Ничья")
            # все случаи бумаги
            if view.player_choice == 3 and bot_choice == 1:
                await mes.edit(content = self.bot.user.mention+" Выбрал камень")
                await interaction.channel.send("Вы победили")
            if view.player_choice == 1 and bot_choice == 3:
                await mes.edit(content = self.bot.user.mention+" Выбрал бумагу")
                await interaction.channel.send("Вы проиграли")
            if view.player_choice == 3 and bot_choice == 3:
                await mes.edit(content = self.bot.user.mention+" Выбрал бумагу")
                await interaction.channel.send("Ничья")
        # все случаи когда время вышло
        if view.player_choice is None:
            await interaction.channel.send("Время вышло...")

class rps_bot(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 10 #таймаут на 10 сек
        self.player_choice = None # игрок делает выбор
   
    @nextcord.ui.button(label="Камень", emoji= "🪨", style=nextcord.ButtonStyle.blurple)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.player_choice = 1
        self.status = True
        self.stop()

    @nextcord.ui.button(label="Ножницы", emoji= "✂", style=nextcord.ButtonStyle.blurple)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.player_choice = 2
        self.status = True
        self.stop()

    @nextcord.ui.button(label="Бумага", emoji= "📄", style=nextcord.ButtonStyle.blurple)
    async def button3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.player_choice = 3
        self.status = True
        self.stop()
            
def setup(bot):
    bot.add_cog(RPCBOT(bot))