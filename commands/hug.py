import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import json

class hug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Hug", dm_permission=False)
    async def hug(self, ctx, *, user_2: nextcord.Member):
        response = requests.get('https://some-random-api.com/animu/hug')
        json_data = json.loads(response.text)
        user_1 = ctx.message.author
        embed = nextcord.Embed(
            title = "Обнимашки",
            colour = nextcord.Color.green(),
            description = "Пользователь "+ user_1.mention+ " обнял "+ user_2.mention+ "."
            )
        embed.set_image(
            url = json_data['link']
            )
        await ctx.send(embed=embed)
    
    @hug.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Выберите пользователя.")

    @nextcord.slash_command(name="hug", description="Обнять пользователя")
    @application_checks.guild_only()
    async def roll_(self, interaction: Interaction, user : nextcord.User = SlashOption(description="Выберите пользователя")):
        response = requests.get('https://some-random-api.com/animu/hug')
        json_data = json.loads(response.text)
        user_1 = interaction.user
        embed = nextcord.Embed(
            title = "Обнимашки",
            colour = nextcord.Color.green(),
            description = "Пользователь "+ user_1.mention+ " обнял "+ user.mention+ "."
            )
        embed.set_image(
            url = json_data['link']
            )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(hug(bot))