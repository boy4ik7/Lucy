import nextcord
from nextcord.ext import commands

# помощь (список доступных команд)
class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Info", dm_permission=False)
    async def info(self, ctx):
        embed = nextcord.Embed(
                title = "Lucy BOT",
                colour = nextcord.Color.green(),
                description = "**Бот для проигрывания музыки и развлечений.**\n"
                "[Присоединяйтесь](https://discord.gg/PAzgmJZ4jS) к серверу, чтобы следить за обновлениями\n"
                )
        embed.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/1089234712834363392/1099425502994890783/55851061-078a-419b-a0bb-5b056d76d5d6-0.png"
            )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(info(bot))
