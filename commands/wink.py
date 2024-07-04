import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import json

class wink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Подмигнуть ... или [кому]", dm_permission=False)
    async def wink(self, ctx, *, user_2: nextcord.Member = None):
        response = requests.get('https://some-random-api.com/animu/wink') # стало "https://some-random-api.com" было "https://some-random-api.ml"
        json_data = json.loads(response.text)
        user_1 = ctx.message.author
        if user_2 in ctx.guild.members:
            embed = nextcord.Embed(
                title = "Подмигнул",
                colour = nextcord.Color.random(),
                description = "Пользователь "+ user_1.mention+ " подмигивает "+ user_2.mention+ "."
                )
            embed.set_image(
                url = json_data['link']
                )
        else:
            embed = nextcord.Embed(
                title = "Подмигнул",
                colour = nextcord.Color.random(),
                description = "Пользователь "+ user_1.mention+ " подмигивает."
                )
            embed.set_image(
                url = json_data['link']
                )
        await ctx.send(embed = embed)
    
    @wink.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Выберите пользователя или не выбирайте вовсе.")
    
    @nextcord.slash_command(name="wink", description="Подмигнуть, пользователь не обязателен")
    @application_checks.guild_only()
    async def roll_(self, interaction: Interaction, user : nextcord.User = SlashOption(description="Выберите пользователя", required=False)):
        response = requests.get('https://some-random-api.com/animu/wink')
        json_data = json.loads(response.text)
        user_1 = interaction.user
        if user is not None:
            embed = nextcord.Embed(
                title = "Подмигнул",
                colour = nextcord.Color.random(),
                description = "Пользователь "+ user_1.mention+ " подмигивает "+ user.mention+ "."
                )
            embed.set_image(
                url = json_data['link']
                )
        else:
            embed = nextcord.Embed(
                title = "Подмигнул",
                colour = nextcord.Color.random(),
                description = "Пользователь "+ user_1.mention+ " подмигивает."
                )
            embed.set_image(
                url = json_data['link']
                )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(wink(bot))