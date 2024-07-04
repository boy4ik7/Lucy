import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import random

dice = ['<:1_white:1089168042082185301>',
        '<:2_white:1089168047077597284>',
        '<:3_white:1089168053159329863>',
        '<:4_white:1089168057500446793>',
        '<:5_white:1089168060595843112>',
        '<:6_white:1089168066392379563>']
# крэпс (игра в кости)
class craps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @nextcord.slash_command(description="Крэпс 🎲")
    async def craps(self, interaction: Interaction):
        user_interaction = interaction.user
        dice_1 = None
        dice_2 = None
        choice_dice_1 = random.choice(dice)
        choice_dice_2 = random.choice(dice)
        # кость 1
        if choice_dice_1 == '<:1_white:1089168042082185301>':
            dice_1 = 1
        if choice_dice_1 == '<:2_white:1089168047077597284>':
            dice_1 = 2
        if choice_dice_1 == '<:3_white:1089168053159329863>':
            dice_1 = 3
        if choice_dice_1 == '<:4_white:1089168057500446793>':
            dice_1 = 4
        if choice_dice_1 == '<:5_white:1089168060595843112>':
            dice_1 = 5
        if choice_dice_1 == '<:6_white:1089168066392379563>':
            dice_1 = 6
        # кость 2
        if choice_dice_2 == '<:1_white:1089168042082185301>':
            dice_2 = 1
        if choice_dice_2 == '<:2_white:1089168047077597284>':
            dice_2 = 2
        if choice_dice_2 == '<:3_white:1089168053159329863>':
            dice_2 = 3
        if choice_dice_2 == '<:4_white:1089168057500446793>':
            dice_2 = 4
        if choice_dice_2 == '<:5_white:1089168060595843112>':
            dice_2 = 5
        if choice_dice_2 == '<:6_white:1089168066392379563>':
            dice_2 = 6
        checkpoint_sum = None
        sum_dice = dice_1 + dice_2
        view = craps_Button(checkpoint_sum, sum_dice, user_interaction)
        if sum_dice == 11 or sum_dice == 7:
            await interaction.response.send_message(choice_dice_1+choice_dice_2,view=view)
            await interaction.channel.send("Вы выиграли!")
        elif sum_dice == 2 or sum_dice == 8 or sum_dice == 12:
            await interaction.response.send_message(choice_dice_1+choice_dice_2,view=view)
            await interaction.channel.send("Вы проиграли!")
        else:
            checkpoint_sum = sum_dice
            await interaction.response.send_message(choice_dice_1+choice_dice_2,view=view)
            await interaction.channel.send("Чекпоинт! Бросайте ещё.")
    

class craps_Button(nextcord.ui.View):
    def __init__(self, checkpoint_sum, sum_dice, user_interaction):
        super().__init__()
        self.timeout = 10 # таймаут на 10 сек
        self.checkpoint_sum = checkpoint_sum
        self.sum_dice = sum_dice
        self.user_interaction = user_interaction

    @nextcord.ui.button(label="Правила ❓", style=nextcord.ButtonStyle.blurple)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Игрок бросает две кости и подсчитывает сумму набранных очков. Если она 7 или 11, то он выиграл, если - 2,8,12, то проиграл. Если выпала другая сумма - его пойнт. Если выпадает пойнт, то игрок бросает кости до тех пор, пока не выпадет 7 - это означает проигрыш или пока не выпадет пойнт - игрок выиграл.", ephemeral=True)

    @nextcord.ui.button(label="Перебросить 🎲", style=nextcord.ButtonStyle.blurple)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
         if interaction.user == self.user_interaction:
            if self.sum_dice == 7 or self.sum_dice == 11:
                await interaction.response.send_message("Вы уже выиграли.", ephemeral=True)
                self.stop()
            elif self.sum_dice == self.sum_dice == 2 or self.sum_dice == 8 or self.sum_dice == 12:
                await interaction.response.send_message("Вы уже проиграли.", ephemeral=True)
                self.stop()
            else:
                if self.sum_dice == self.checkpoint_sum:
                    await interaction.response.send_message("Вы уже выиграли.", ephemeral=True)
                    self.stop()
                if self.sum_dice == 7:
                    await interaction.response.send_message("Вы уже проиграли.", ephemeral=True)
                    self.stop()
                else:
                    dice_1 = None
                    dice_2 = None
                    choice_dice_1 = random.choice(dice)
                    choice_dice_2 = random.choice(dice)
                    # кость 1
                    if choice_dice_1 == '<:1_white:1089168042082185301>':
                        dice_1 = 1
                    if choice_dice_1 == '<:2_white:1089168047077597284>':
                        dice_1 = 2
                    if choice_dice_1 == '<:3_white:1089168053159329863>':
                        dice_1 = 3
                    if choice_dice_1 == '<:4_white:1089168057500446793>':
                        dice_1 = 4
                    if choice_dice_1 == '<:5_white:1089168060595843112>':
                        dice_1 = 5
                    if choice_dice_1 == '<:6_white:1089168066392379563>':
                        dice_1 = 6
                    # кость 2
                    if choice_dice_2 == '<:1_white:1089168042082185301>':
                        dice_2 = 1
                    if choice_dice_2 == '<:2_white:1089168047077597284>':
                        dice_2 = 2
                    if choice_dice_2 == '<:3_white:1089168053159329863>':
                        dice_2 = 3
                    if choice_dice_2 == '<:4_white:1089168057500446793>':
                        dice_2 = 2
                    if choice_dice_2 == '<:5_white:1089168060595843112>':
                        dice_2 = 5
                    if choice_dice_2 == '<:6_white:1089168066392379563>':
                        dice_2 = 6    
                    self.sum_dice = dice_1 + dice_2
                    #print(self.dice_sum)
                    if self.sum_dice == 7:
                        await interaction.response.send_message(choice_dice_1+choice_dice_2)
                        await interaction.channel.send("Вы проиграли!")
                    elif self.sum_dice == self.checkpoint_sum:
                        await interaction.response.send_message(choice_dice_1+choice_dice_2)
                        await interaction.channel.send("Вы выиграли!")
                    else:
                        await interaction.response.send_message(choice_dice_1+choice_dice_2)
                        checkpoint_sum = self.checkpoint_sum
                        sum_dice = self.sum_dice
                        user_interaction = self.user_interaction
                        viev = craps_Button(checkpoint_sum, sum_dice, user_interaction)
                        await interaction.channel.send("Бросайте ещё.", view=viev)
         else:
            await interaction.response.send_message("Играет другой игрок", ephemeral=True)

def setup(bot):
    bot.add_cog(craps(bot))