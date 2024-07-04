import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import json

class pat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Погладить [кого]", dm_permission=False)
    async def pat(self, ctx, *, user_2: nextcord.Member):
        response = requests.get('https://some-random-api.com/animu/pat')
        json_data = json.loads(response.text)
        user_1 = ctx.message.author
        embed = nextcord.Embed(
            title = "Погладил",
            colour = nextcord.Color.blue(),
            description = "Пользователь "+ user_1.mention+ " гладит "+ user_2.mention+ "."
            )
        embed.set_image(
            url = json_data['link']
            )
        await ctx.send(embed = embed)
    
    @pat.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Выберите пользователя.")

    @nextcord.slash_command(name="pat", description="Погладить пользователя")
    @application_checks.guild_only()
    async def roll_(self, interaction: Interaction, user : nextcord.User = SlashOption(description="Выберите пользователя")):
        response = requests.get('https://some-random-api.com/animu/pat')
        json_data = json.loads(response.text)
        user_1 = interaction.user
        embed = nextcord.Embed(
            title = "Погладил",
            colour = nextcord.Color.blue(),
            description = "Пользователь "+ user_1.mention+ " гладит "+ user.mention+ "."
            )
        embed.set_image(
            url = json_data['link']
            )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(pat(bot))