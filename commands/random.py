import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import random
import requests
import asyncio

dice_1 = ['<:1_white:1089168042082185301>',
        '<:2_white:1089168047077597284>',
        '<:3_white:1089168053159329863>',
        '<:4_white:1089168057500446793>',
        '<:5_white:1089168060595843112>',
        '<:6_white:1089168066392379563>']

dice_2 = ['<:1_black:1089168035174170734>',
        '<:2_black:1089168045378904095>',
        '<:3_black:1089168050579841106>',
        '<:4_black:1089168054895788194>',
        '<:5_black:1089168058729386077>',
        '<:6_black:1089168063267606668>']

dice_ = ['<:1_d20:1139506995347587152>',
        '<:2_d20:1139506999655145563>',
        '<:3_d20:1139507003782332436>',
        '<:4_d20:1139507006454112256>',
        '<:5_d20:1139507009960546414>',
        '<:6_d20:1139507013546692700>',
        '<:7_d20:1139507016130375792>',
        '<:8_d20:1139507019318042664>',
        '<:9_d20:1139507026549031013>',
        '<:10_d20:1139507030000934975>',
        '<:11_d20:1139507032781758534>',
        '<:12_d20:1139507036258840637>',
        '<:13_d20:1139507040369250315>',
        '<:14_d20:1139507043435290695>',
        '<:15_d20:1139507047579263017>',
        '<:16_d20:1139507055275802794>',
        '<:17_d20:1139507063869935746>',
        '<:18_d20:1139507070048157696>',
        '<:19_d20:1139507076926816357>',
        '<:20_d20:1139507087504838686>']


class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_numbers(self, min, max):
        url = f"https://www.random.org/integers/?num=1&min={min}&max={max}&col=1&base=10&format=plain&rnd=new"
        response = requests.get(url)
        if response.status_code == 200:
            return int(response.text.strip())
        else:
            return None
    # кости
    @nextcord.slash_command(name="dice", description="Бросить кости 🎲 (2d6)")
    @application_checks.guild_only()
    async def d4_(self, interaction: Interaction):
        await interaction.response.defer()
        num_1 = self.get_numbers(min=0, max=5)
        await asyncio.sleep(1)
        num_2 = self.get_numbers(min=0, max=5)
        if num_1 is None or num_2 is None:
            choice_dice_1 = random.choice(dice_1)
            choice_dice_2 = random.choice(dice_2)
        else:
            choice_dice_1 = dice_1[num_1]
            choice_dice_2 = dice_2[num_2]
        await interaction.followup.send(choice_dice_1+choice_dice_2)
    # d20
    @nextcord.slash_command(description="Бросить икосаэдр (d20)")
    @application_checks.guild_only()
    async def d20(self, interaction: Interaction):
        await interaction.response.defer()
        num = self.get_numbers(min=1, max=20)
        if num is None:
            choice_dice = random.choice(dice)
        else:
            choice_dice = dice_[num]
        await interaction.followup.send(choice_dice)
    #roll
    @nextcord.slash_command(name="roll", description="Случайный вибор из списка")
    @application_checks.guild_only()
    async def roll_(self, interaction: Interaction, list: str = SlashOption(description="Список, через запятую")):
        await interaction.response.defer()
        comma = ','
        list_choice = list.split(comma)
        max = len(list_choice) - 1
        num = self.get_numbers(min=0, max=max) 
        if num is None:
            choice = random.choice(list_choice)
        else:
            choice = list_choice[num]
        await interaction.followup.send(choice)

    #random
    @nextcord.slash_command(description="Случайный вибор числа")
    @application_checks.guild_only()
    async def random(self, interaction: Interaction, min: str = SlashOption(description="Минимальное число"), max: str = SlashOption(description="Максимальное число")):
        await interaction.response.defer()
        try:
            min = int(min)
            max = int(max)
            choice = self.get_numbers(min=min, max=max) 
            if choice is None:
                choice = random.randint(min, max)
            await interaction.followup.send(f"# {choice}")
        except:
            await interaction.followup.send("Ошибка, проверьте числа.", ephemeral=True)

def setup(bot):
    bot.add_cog(dice(bot))