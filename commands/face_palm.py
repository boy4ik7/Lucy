import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import requests
import json

class face_palm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Face palm", dm_permission=False)
    async def face_palm(self, ctx):
        response = requests.get('https://some-random-api.com/animu/face-palm')
        json_data = json.loads(response.text)
        user_1 = ctx.message.author
        embed = nextcord.Embed(
            title = "Face palm",
            colour = nextcord.Color.dark_gray(),
            description = "Пользователь "+ user_1.mention+ " прикрывает лицо рукой..."
            )
        embed.set_image(
            url = json_data['link']
            )
        await ctx.send(embed = embed)
    
    @nextcord.slash_command(name="face_palm", description="Прикрыть лицо рукой")
    @application_checks.guild_only()
    async def roll_(self, interaction: Interaction):
        response = requests.get('https://some-random-api.com/animu/face-palm')
        json_data = json.loads(response.text)
        user_1 = interaction.user
        embed = nextcord.Embed(
            title = "Face palm",
            colour = nextcord.Color.dark_gray(),
            description = "Пользователь "+ user_1.mention+ " прикрывает лицо рукой..."
            )
        embed.set_image(
            url = json_data['link']
            )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(face_palm(bot))