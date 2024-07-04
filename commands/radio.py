import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import asyncio
# v1
log_channel = 1107761340031979592
TESTING_GUILD_ID = 1089166037934669966 # Lucy BOT

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
server_data = {}

def get_server_data(server_id):
    if server_id not in server_data:
        add_server(server_id)
    return server_data[server_id]

def add_server(server_id):
    server_data[server_id] = {
        'vc': None
    }

async def play(interaction, url):
    await interaction.response.defer()
    bot_voice_state = interaction.guild.voice_client
    server_id = interaction.guild.id
    server_data = get_server_data(server_id)
    try:
        try:
            if server_data['vc'].is_playing():
                server_data['vc'].pause()
        except:
            pass
        if not (bot_voice_state is not None and bot_voice_state.channel is not None):
            channel = interaction.user.voice.channel
            server_data['vc'] = await channel.connect()
        server_data['vc'].play(nextcord.FFmpegPCMAudio(url))
        view = playback_button(timeout=18000)
        user = interaction.user
        await interaction.followup.send(f"Играет: ``{url}``\nОт: {user.mention}", view=view)
        timer = 0
        while server_data['vc'].is_playing() or server_data['vc'].is_paused():
            await asyncio.sleep(1)
            timer += 1
            if timer > 18000:
                await interaction.channel.send("Бот находится в канале более 5-ти часов, если вы не дослушали поставьте пожалуйста снова.")
                break
        await server_data['vc'].disconnect()
        if timer < 10:
            await interaction.channel.send("*Проверьте правильность ссылки.*")
    except:
        await interaction.followup.send("*Проверьте правильность ссылки.*")
        print(f"Ссылка на аудиопоток не доступна: {url}")

async def leave(interaction):
    voice_state = interaction.user.voice
    if voice_state is not None and voice_state.channel is not None:
        guild = interaction.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        #await interaction.response.send_message("Бот остановлен.")
    else:
        await interaction.response.send_message("Вы не находитесь в голосовом канале.")

class add_url_button(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 120

    @nextcord.ui.button(label="Добавить поток", style=nextcord.ButtonStyle.green)
    async def button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            modal = text_in()
            await interaction.response.send_modal(modal)
            self.stop()
        else:
            await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

class playback_button(nextcord.ui.View):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
    # stop
    @nextcord.ui.button(label="⏹", style=nextcord.ButtonStyle.red)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            await leave(interaction)
            self.stop()
        else:
            await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

    # +
    @nextcord.ui.button(label="➕", style=nextcord.ButtonStyle.green)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            modal = text_in()
            await interaction.response.send_modal(modal)
            self.stop()
        else:
            await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

class text_in(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Добавление потока",
            timeout= 300,
        )

        self.name = nextcord.ui.TextInput(
            label="Введите ссылку: ",
            min_length=1,
            max_length=2000,
        )
        self.add_item(self.name)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        url = self.name.value
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            await play(interaction, url)
        else:
            await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)

class radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="radio", description="Проигрывание онлайн потоков")
    async def radio(self, interaction: Interaction, url : str = SlashOption(description="Ссылка на поток", required=False)):
        voice_state = interaction.user.voice
        if voice_state is not None and voice_state.channel is not None:
            if url is not None:
                await play(interaction, url)
            else:
                view = add_url_button()
                await interaction.response.send_message("Cсылки на потоки можно найти здесь: \nhttps://streamurl.link \nhttps://www.fmlist.org \nhttps://fmstream.org", view=view)#, ephemeral=True)
        else:
            await interaction.response.send_message("Вы не находитесь в голосовом канале.", ephemeral=True)
    
def setup(bot):
    bot.add_cog(radio(bot))
