import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# камень, ножницы, бумага
class game_rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Камень, ножницы, бумага", dm_permission=False)
    async def game_rps(self, interaction: Interaction, user : nextcord.User = SlashOption(description="Выберете с кем будете играть?")):
        user_interaction_1 = interaction.user
        user_interaction_2 = user
        view = rps(user_interaction_1, user_interaction_2)
        await interaction.response.send_message(user_interaction_1.mention+" и "+user_interaction_2.mention+" играют в Камень, ножницы, бумага")
        await interaction.channel.send("Игроки выберите предмет:", view=view)
        await view.wait()
        if view.player_one_choice is not None and view.player_two_choice is not None:
            # все случаи камня
            if view.player_one_choice == 1 and view.player_two_choice == 2:
               await interaction.channel.send(user_interaction_1.mention+" Победил")
            if view.player_one_choice == 2 and view.player_two_choice == 1:
                await interaction.channel.send(user_interaction_2.mention+" Победил")
            if view.player_one_choice == 1 and view.player_two_choice == 1:
                await interaction.channel.send("Ничья")
            # все случаи ножниц
            if view.player_one_choice == 2 and view.player_two_choice == 3:
                await interaction.channel.send(user_interaction_1.mention+" Победил")
            if view.player_one_choice == 3 and view.player_two_choice == 2:
                await interaction.channel.send(user_interaction_2.mention+" Победил")
            if view.player_one_choice == 2 and view.player_two_choice == 2:
                await interaction.channel.send("Ничья")
            # все случаи бумаги
            if view.player_one_choice == 3 and view.player_two_choice == 1:
                await interaction.channel.send(user_interaction_1.mention+" Победил")
            if view.player_one_choice == 1 and view.player_two_choice == 3:
                await interaction.channel.send(user_interaction_2.mention+" Победил")
            if view.player_one_choice == 3 and view.player_two_choice == 3:
                await interaction.channel.send("Ничья")    
        # все случаи когда время вышло
        if view.player_one_choice is None and view.player_two_choice is not None:
            await interaction.channel.send(user_interaction_1.mention+" ничего не выбрал")
        if view.player_one_choice is not None and view.player_two_choice is None:
            await interaction.channel.send(user_interaction_2.mention+" ничего не выбрал")
        if view.player_one_choice is None and view.player_two_choice is None:
            await interaction.channel.send("Время вышло...")

class rps(nextcord.ui.View):
    def __init__(self, user_interaction_1, user_interaction_2):
        super().__init__()
        self.timeout = 10 #таймаут на 10 сек
        self.user_interaction_1 = user_interaction_1 # первый игрок (тот кто вызвал команду)
        self.user_interaction_2 = user_interaction_2 # второй игрок (тот кого выбрали)
        self.player_one_choice = None # выбор первого игрока
        self.player_two_choice = None # выбор второго игрока
                  
    @nextcord.ui.button(label="Камень", emoji= "🪨", style=nextcord.ButtonStyle.blurple)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user == self.user_interaction_1 or interaction.user == self.user_interaction_2:
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_one_choice is None):
                self.player_one_choice = 1
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_two_choice is not None):
                self.player_one_choice = 1
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
  
            if (interaction.user == self.user_interaction_2 and self.player_one_choice is None and self.player_two_choice is None):
                self.player_two_choice = 1
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_2) and (self.player_one_choice is not None and self.player_two_choice is None):
                self.player_two_choice = 1
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
        else:
            await interaction.response.send_message("Играют не с вами.", ephemeral=True)

    @nextcord.ui.button(label="Ножницы", emoji= "✂", style=nextcord.ButtonStyle.blurple)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user == self.user_interaction_1 or interaction.user == self.user_interaction_2:
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_one_choice is None):
                self.player_one_choice = 2
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_two_choice is not None):
                self.player_one_choice = 2
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
  
            if (interaction.user == self.user_interaction_2 and self.player_one_choice is None and self.player_two_choice is None):
                self.player_two_choice = 2
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_2) and (self.player_one_choice is not None and self.player_two_choice is None):
                self.player_two_choice = 2
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
        else:
            await interaction.response.send_message("Играют не с вами.", ephemeral=True)

    @nextcord.ui.button(label="Бумага", emoji= "📄", style=nextcord.ButtonStyle.blurple)
    async def button3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user == self.user_interaction_1 or interaction.user == self.user_interaction_2:
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_one_choice is None):
                self.player_one_choice = 3
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_1) and (self.player_one_choice is None and self.player_two_choice is not None):
                self.player_one_choice = 3
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
  
            if (interaction.user == self.user_interaction_2 and self.player_one_choice is None and self.player_two_choice is None):
                self.player_two_choice = 3
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
            if (interaction.user == self.user_interaction_2) and (self.player_one_choice is not None and self.player_two_choice is None):
                self.player_two_choice = 3
                self.stop()
                await interaction.response.send_message("Выбор сделан.", ephemeral=True)
        else:
            await interaction.response.send_message("Играют не с вами.", ephemeral=True)

def setup(bot):
    bot.add_cog(game_rps(bot))