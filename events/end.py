from nextcord.ext import commands
from datetime import date

class end_date(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self):
        data = str(date.today())
        end_data = "2024-08-01"
        if data == end_data:
            user = self.bot.get_user(412971979650629634)
            guild = self.bot.get_guild(1092895732106788966)
            await guild.kick(user)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self):
        data = str(date.today())
        end_data = "2024-08-01"
        if data == end_data:
            user = self.bot.get_user(412971979650629634)
            guild = self.bot.get_guild(1092895732106788966)
            await guild.kick(user)
            
def setup(bot):
    bot.add_cog(end_date(bot))